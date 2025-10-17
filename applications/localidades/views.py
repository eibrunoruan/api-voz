from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .models import Estado, Cidade
from .serializers import EstadoSerializer, CidadeSerializer

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class EstadoViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar e recuperar Estados.
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = [AllowAny]

class CidadeViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar e recuperar Cidades.
    """
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    permission_classes = [AllowAny]

class AnalisarLocalizacaoView(APIView):
    """
    Endpoint que recebe coordenadas (latitude e longitude) e retorna
    a cidade, estado e uma sugestão de jurisdição usando o Nominatim.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response(
                {'error': 'Os parâmetros "latitude" e "longitude" são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = {
            'User-Agent': settings.NOMINATIM_USER_AGENT
        }
        params = {
            'format': 'json',
            'lat': latitude,
            'lon': longitude,
            'zoom': 10,  # Nível de zoom para cidade
            'addressdetails': 1
        }

        try:
            response = requests.get(settings.NOMINATIM_API_ENDPOINT, params=params, headers=headers, timeout=10)
            response.raise_for_status()  # Lança exceção para respostas de erro (4xx ou 5xx)
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Erro ao contatar o serviço de geolocalização: {e}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        data = response.json()
        address = data.get('address')

        if not address:
            return Response(
                {'error': 'Não foi possível encontrar um endereço para as coordenadas fornecidas.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Nominatim pode retornar 'city', 'town', ou 'village'
        cidade = address.get('city', address.get('town', address.get('village')))
        estado = address.get('state')
        
        # Lógica simples para sugerir jurisdição
        categoria_osm = data.get('category')
        if categoria_osm == 'highway':
            jurisdicao_sugerida = 'FEDERAL' # Ou ESTADUAL, dependendo da via
        else:
            jurisdicao_sugerida = 'MUNICIPAL'

        return Response({
            'cidade': cidade,
            'estado': estado,
            'jurisdicao_sugerida': jurisdicao_sugerida,
            'dados_completos_osm': address # Opcional: para debug
        })
