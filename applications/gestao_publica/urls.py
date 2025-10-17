from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    MinhasDenunciasViewSet, 
    OfficialResponseViewSet, 
    DashboardView,
    DenunciasPorPeriodoView,
    HeatmapView
)

app_name = 'gestao_publica'

router = DefaultRouter()
router.register(r'minhas-denuncias', MinhasDenunciasViewSet, basename='minhas-denuncias')
router.register(r'respostas', OfficialResponseViewSet, basename='respostas')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/denuncias-por-periodo/', DenunciasPorPeriodoView.as_view(), name='dashboard-denuncias-por-periodo'),
    path('dashboard/heatmap/', HeatmapView.as_view(), name='dashboard-heatmap'),
] + router.urls