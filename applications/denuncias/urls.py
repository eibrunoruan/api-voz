from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, DenunciaViewSet, ApoioDenunciaViewSet

# Cria um router e registra nossas viewsets com ele.
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'denuncias', DenunciaViewSet, basename='denuncia')
router.register(r'apoios', ApoioDenunciaViewSet, basename='apoio')

# As URLs da API são determinadas automaticamente pelo router.
urlpatterns = [
    path('', include(router.urls)),
]