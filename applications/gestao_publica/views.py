from rest_framework import viewsets, permissions, mixins, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear
from datetime import datetime

from applications.denuncias.models import Denuncia
from applications.denuncias.serializers import DenunciaSerializer
from .serializers import OfficialResponseSerializer
from .models import OfficialResponse


class MinhasDenunciasViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint da API que retorna as denúncias relevantes para o gestor público logado.
    Filtra as denúncias com base na entidade governamental associada ao gestor.
    """
    serializer_class = DenunciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, 'tipo_usuario') or user.tipo_usuario != 'GESTOR_PUBLICO':
            return Denuncia.objects.none()

        entidade_gerenciada = user.entidades_gerenciadas.first()
        if not entidade_gerenciada:
            return Denuncia.objects.none()

        if entidade_gerenciada.cidade:
            return Denuncia.objects.filter(
                cidade=entidade_gerenciada.cidade,
                jurisdicao=Denuncia.Jurisdicao.MUNICIPAL
            )
        elif entidade_gerenciada.estado:
            return Denuncia.objects.filter(
                estado=entidade_gerenciada.estado,
                jurisdicao=Denuncia.Jurisdicao.ESTADUAL
            )
        
        return Denuncia.objects.none()


class CanRespondToDenuncia(permissions.BasePermission):
    """
    Permissão para garantir que um gestor só pode responder a uma denúncia
    que pertence à sua jurisdição.
    """
    message = "Você não tem permissão para responder a esta denúncia ou a denúncia não foi encontrada."

    def has_permission(self, request, view):
        if view.action != 'create':
            return True

        user = request.user
        denuncia_id = request.data.get('denuncia')

        if not denuncia_id:
            self.message = "O ID da denúncia ('denuncia') é obrigatório no corpo da requisição."
            return False

        if not hasattr(user, 'tipo_usuario') or user.tipo_usuario != 'GESTOR_PUBLICO':
            return False

        entidade_gerenciada = user.entidades_gerenciadas.first()
        if not entidade_gerenciada:
            return False

        denuncias_permitidas = Denuncia.objects.none()
        if entidade_gerenciada.cidade:
            denuncias_permitidas = Denuncia.objects.filter(
                cidade=entidade_gerenciada.cidade,
                jurisdicao=Denuncia.Jurisdicao.MUNICIPAL
            )
        elif entidade_gerenciada.estado:
            denuncias_permitidas = Denuncia.objects.filter(
                estado=entidade_gerenciada.estado,
                jurisdicao=Denuncia.Jurisdicao.ESTADUAL
            )

        return denuncias_permitidas.filter(pk=denuncia_id).exists()


class OfficialResponseViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    ViewSet para criar, listar e ver OfficialResponse.
    - A criação de uma resposta é restrita a gestores da jurisdição correta.
    - A listagem retorna apenas as respostas da entidade do gestor logado.
    """
    serializer_class = OfficialResponseSerializer
    permission_classes = [permissions.IsAuthenticated, CanRespondToDenuncia]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario == 'GESTOR_PUBLICO':
            entidade = user.entidades_gerenciadas.first()
            if entidade:
                return OfficialResponse.objects.filter(entidade=entidade)
        return OfficialResponse.objects.none()

    def perform_create(self, serializer):
        entidade = self.request.user.entidades_gerenciadas.first()
        
        # O modelo já garante que a denúncia só pode ter uma resposta (OneToOneField),
        # então o banco de dados vai gerar um erro de integridade se tentarem criar uma segunda.
        serializer.save(entidade=entidade)


class DashboardView(APIView):
    """
    Endpoint que retorna dados estatísticos para o dashboard do gestor público.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'tipo_usuario') or user.tipo_usuario != 'GESTOR_PUBLICO':
            return Response(
                {'error': 'Apenas gestores públicos podem acessar o dashboard.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Reutiliza a lógica de filtragem do MinhasDenunciasViewSet
        denuncias_queryset = MinhasDenunciasViewSet().get_queryset(self.request)

        if not denuncias_queryset.exists():
            return Response({
                'total_denuncias': 0,
                'status_counts': {},
                'categoria_counts': {},
            })

        # Calcula o total de denúncias
        total_denuncias = denuncias_queryset.count()

        # Calcula a contagem por status
        status_counts_query = denuncias_queryset.values('status').annotate(count=Count('status')).order_by('-count')
        status_counts = {item['status']: item['count'] for item in status_counts_query}

        # Calcula a contagem por categoria
        categoria_counts_query = denuncias_queryset.values('categoria__nome').annotate(count=Count('categoria__nome')).order_by('-count')
        categoria_counts = {item['categoria__nome']: item['count'] for item in categoria_counts_query}

        data = {
            'total_denuncias': total_denuncias,
            'status_counts': status_counts,
            'categoria_counts': categoria_counts,
        }

        return Response(data)


class DenunciasPorPeriodoView(APIView):
    """
    Endpoint que retorna a contagem de denúncias agrupadas por um período de tempo.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'tipo_usuario') or user.tipo_usuario != 'GESTOR_PUBLICO':
            return Response(
                {'error': 'Apenas gestores públicos podem acessar este endpoint.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Define os possíveis agrupamentos e suas funções Trunc correspondentes
        periodo_mapping = {
            'dia': TruncDay,
            'semana': TruncWeek,
            'mes': TruncMonth,
            'trimestre': TruncQuarter,
            'ano': TruncYear,
        }

        periodo = request.query_params.get('periodo', 'dia').lower()
        if periodo not in periodo_mapping:
            return Response(
                {'error': f'Valor inválido para "periodo". Opções: {list(periodo_mapping.keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reutiliza a lógica de filtragem do MinhasDenunciasViewSet
        base_queryset = MinhasDenunciasViewSet().get_queryset(self.request)

        # Filtra por data, se fornecido
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        if start_date_str:
            base_queryset = base_queryset.filter(data_criacao__gte=datetime.fromisoformat(start_date_str))
        if end_date_str:
            base_queryset = base_queryset.filter(data_criacao__lte=datetime.fromisoformat(end_date_str))

        # Aplica a função de truncagem dinamicamente
        trunc_function = periodo_mapping[periodo]('data_criacao')

        # Realiza a agregação
        queryset = (
            base_queryset
            .annotate(periodo_agrupado=trunc_function)
            .values('periodo_agrupado')
            .annotate(total=Count('id'))
            .order_by('periodo_agrupado')
        )

        # Formata a saída
        data = [
            {
                "data": item['periodo_agrupado'].strftime('%Y-%m-%d'), 
                "total": item['total']
            } 
            for item in queryset
        ]
        return Response(data)


class HeatmapView(APIView):
    """
    Endpoint que retorna dados para a geração de um mapa de calor.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not hasattr(user, 'tipo_usuario') or user.tipo_usuario != 'GESTOR_PUBLICO':
            return Response(
                {'error': 'Apenas gestores públicos podem acessar este endpoint.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Reutiliza a lógica de filtragem do MinhasDenunciasViewSet
        base_queryset = MinhasDenunciasViewSet().get_queryset(self.request)

        # Anota o peso como 1 (denúncia original) + número de apoios
        heatmap_data = (
            base_queryset
            .annotate(apoios_count=Count('apoios'))
            .annotate(weight=F('apoios_count') + 1)
            .values('latitude', 'longitude', 'weight')
        )

        return Response(list(heatmap_data))