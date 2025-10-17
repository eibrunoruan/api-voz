from django.contrib import admin
from .models import Estado, Cidade

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    """Configuração do Admin para o modelo Estado."""
    list_display = ('nome', 'uf')
    search_fields = ('nome', 'uf')

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    """Configuração do Admin para o modelo Cidade."""
    list_display = ('nome', 'estado')
    search_fields = ('nome',)
    list_filter = ('estado',)
    # Melhora a performance para carregar o ForeignKey de estado
    list_select_related = ('estado',)