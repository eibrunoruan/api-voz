from rest_framework import permissions
from applications.denuncias.models import Denuncia

class IsGestorWithJurisdiction(permissions.BasePermission):
    """
    Permissão para garantir que um usuário seja um gestor público
    e tenha jurisdição sobre a denúncia que está tentando modificar.
    """
    message = "Você não tem permissão para executar esta ação nesta denúncia."

    def has_object_permission(self, request, view, obj):
        # Garante que o objeto é uma instância de Denuncia
        if not isinstance(obj, Denuncia):
            return False

        user = request.user

        # Verifica se o usuário é um gestor público
        if not hasattr(user, 'tipo_usuario') or user.tipo_usuario != 'GESTOR_PUBLICO':
            return False

        # Obtém a primeira entidade gerenciada pelo gestor
        entidade_gerenciada = user.entidades_gerenciadas.first()
        if not entidade_gerenciada:
            return False

        # Compara a jurisdição da denúncia com a da entidade do gestor
        if entidade_gerenciada.cidade:
            return obj.cidade == entidade_gerenciada.cidade and obj.jurisdicao == Denuncia.Jurisdicao.MUNICIPAL
        
        if entidade_gerenciada.estado:
            return obj.estado == entidade_gerenciada.estado and obj.jurisdicao == Denuncia.Jurisdicao.ESTADUAL

        return False
