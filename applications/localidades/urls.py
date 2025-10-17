from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstadoViewSet, CidadeViewSet, AnalisarLocalizacaoView

router = DefaultRouter()
router.register(r'estados', EstadoViewSet, basename='estado')
router.register(r'cidades', CidadeViewSet, basename='cidade')

urlpatterns = [
    path('', include(router.urls)),
    path('analisar/', AnalisarLocalizacaoView.as_view(), name='analisar-localizacao'),
]
