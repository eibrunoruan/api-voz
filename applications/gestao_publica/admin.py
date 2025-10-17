from django.contrib import admin
from .models import OfficialEntity, OfficialResponse

@admin.register(OfficialEntity)
class OfficialEntityAdmin(admin.ModelAdmin):
    """Configuração do Admin para OfficialEntity."""
    list_display = ('nome', 'cidade', 'estado')
    search_fields = ('nome', 'cidade__nome', 'estado__nome')
    list_filter = ('estado',)
    # Melhora a UI para selecionar gestores
    filter_horizontal = ('gestores',)
    list_select_related = ('cidade', 'estado')

@admin.register(OfficialResponse)
class OfficialResponseAdmin(admin.ModelAdmin):
    """Configuração do Admin para OfficialResponse."""
    list_display = ('denuncia', 'entidade', 'data_resposta')
    search_fields = ('denuncia__titulo', 'entidade__nome')
    list_filter = ('entidade',)
    readonly_fields = ('data_resposta',)
    list_select_related = ('denuncia', 'entidade')