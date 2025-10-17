from rest_framework import serializers
from .models import Estado, Cidade

class EstadoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Estado.
    """
    class Meta:
        model = Estado
        fields = ('id', 'nome', 'uf')

class CidadeSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Cidade.
    """
    class Meta:
        model = Cidade
        fields = ('id', 'nome', 'estado')
