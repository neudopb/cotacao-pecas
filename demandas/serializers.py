from rest_framework import serializers
from demandas.models import Endereco, Contato, Demanda
from accounts.serializers import UsuarioListSerializer

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = '__all__'

class DemandaSerializer(serializers.ModelSerializer):

    endereco  =  EnderecoSerializer()
    contato  =  ContatoSerializer()
    anunciante  =  UsuarioListSerializer()

    class Meta:
        model = Demanda
        fields = '__all__'