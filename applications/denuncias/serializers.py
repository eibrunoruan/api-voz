from rest_framework import serializers
from .models import Categoria, Denuncia, ApoioDenuncia, Comentario
from applications.autenticacao.serializers import UserSerializer

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class DenunciaSerializer(serializers.ModelSerializer):
    autor = UserSerializer(read_only=True)
    total_apoios = serializers.SerializerMethodField()

    class Meta:
        model = Denuncia
        fields = [
            'id', 'titulo', 'descricao', 'autor', 'categoria', 'cidade', 'estado',
            'foto', 'latitude', 'longitude', 'jurisdicao', 'status',
            'data_criacao', 'total_apoios'
        ]
        read_only_fields = ('autor', 'status', 'data_criacao')

    def get_total_apoios(self, obj):
        """
        Calcula o total de apoios recebidos por uma denúncia.
        Este método é eficiente pois a viewset utiliza prefetch_related('apoios').
        """
        return obj.apoios.count()

class ApoioDenunciaSerializer(serializers.ModelSerializer):
    apoiador = UserSerializer(read_only=True)

    class Meta:
        model = ApoioDenuncia
        fields = '__all__'
        read_only_fields = ('apoiador', 'data_apoio')

    def create(self, validated_data):
        validated_data['apoiador'] = self.context['request'].user
        return super().create(validated_data)

class ComentarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Comentario.
    """
    autor = UserSerializer(read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'denuncia', 'autor', 'texto', 'data_criacao']
        read_only_fields = ('id', 'autor', 'data_criacao')