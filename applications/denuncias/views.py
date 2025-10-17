from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.gestao_publica.permissions import IsGestorWithJurisdiction
from .models import Categoria, Denuncia, ApoioDenuncia, Comentario
from .serializers import CategoriaSerializer, DenunciaSerializer, ApoioDenunciaSerializer, ComentarioSerializer
from .services import criar_ou_apoiar_denuncia


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas os donos de um objeto possam editá-lo.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Lida com diferentes nomes de campo de "dono" (autor vs apoiador)
        if hasattr(obj, 'autor'):
            return obj.autor == request.user
        if hasattr(obj, 'apoiador'):
            return obj.apoiador == request.user
        
        return False


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint da API que permite que categorias sejam visualizadas.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class DenunciaViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API que permite que denúncias sejam visualizadas ou editadas.
    """
    queryset = Denuncia.objects.all().select_related(
        'autor', 'categoria', 'cidade', 'estado'
    ).prefetch_related('apoios', 'comentarios')
    serializer_class = DenunciaSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:  # list, retrieve
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        denuncia, created_denuncia, created_apoio = criar_ou_apoiar_denuncia(
            serializer.validated_data, request.user
        )

        response_serializer = self.get_serializer(denuncia)
        headers = self.get_success_headers(response_serializer.data)

        if created_denuncia:
            return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK, headers=headers)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resolver(self, request, pk=None):
        """
        Marca uma denúncia como resolvida. Apenas o autor pode fazer isso.
        """
        denuncia = self.get_object()
        if denuncia.autor != request.user:
            return Response(
                {'detail': 'Apenas o autor pode marcar a denúncia como resolvida.'},
                status=status.HTTP_403_FORBIDDEN
            )

        denuncia.status = Denuncia.Status.RESOLVIDA
        denuncia.save()
        serializer = self.get_serializer(denuncia)
        return Response(serializer.data)

    @action(
        detail=True, 
        methods=['post'], 
        permission_classes=[permissions.IsAuthenticated, IsGestorWithJurisdiction]
    )
    def change_status(self, request, pk=None):
        """
        Permite que um gestor com jurisdição altere o status da denúncia.
        """
        denuncia = self.get_object()
        novo_status = request.data.get('status')

        if not novo_status:
            return Response(
                {'error': 'O campo "status" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Valida se o status enviado é uma opção válida
        status_choices = [choice[0] for choice in Denuncia.Status.choices]
        if novo_status not in status_choices:
            return Response(
                {'error': f'Status inválido. Opções válidas: {status_choices}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        denuncia.status = novo_status
        denuncia.save()
        serializer = self.get_serializer(denuncia)
        return Response(serializer.data)


class ApoioDenunciaViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    Endpoint da API para apoiar uma denúncia.
    """
    serializer_class = ApoioDenunciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ApoioDenuncia.objects.filter(apoiador=self.request.user)

    def perform_create(self, serializer):
        serializer.save(apoiador=self.request.user)


class ComentarioViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    """
    ViewSet para listar, criar e deletar comentários.
    - A listagem é filtrada pelo query param 'denuncia_id'.
    - Apenas o autor de um comentário pode deletá-lo.
    """
    serializer_class = ComentarioSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsOwnerOrReadOnly]
        else: # list, retrieve
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Comentario.objects.select_related('autor').all()
        denuncia_id = self.request.query_params.get('denuncia_id')
        if denuncia_id is not None:
            queryset = queryset.filter(denuncia_id=denuncia_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)