from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Configuração do Admin para o modelo User customizado."""
    # Adiciona o campo 'tipo_usuario' à visualização em lista
    list_display = ('email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff')
    
    # Adiciona 'tipo_usuario' aos filtros da barra lateral
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'groups')
    
    # Campos a serem exibidos no formulário de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )
    
    # Campos a serem exibidos ao criar um novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )
    
    # Define o campo de busca
    search_fields = ('email', 'first_name', 'last_name')
    
    # Define o campo de ordenação padrão
    ordering = ('email',)