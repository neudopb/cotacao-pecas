from rest_framework import serializers
from demandas.models import Endereco, Contato, Demanda
from accounts.serializers import UsuarioListSerializer

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'
        # fields = ('estado', 'cidade', 'endereco', 'numero',)

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = '__all__'
        # fields = ('email', 'telefone',)

class DemandaSerializer(serializers.ModelSerializer):

    endereco  =  EnderecoSerializer()
    contato  =  ContatoSerializer()
    anunciante  =  UsuarioListSerializer()

    class Meta:
        model = Demanda
        fields = '__all__'
        # fields = ('descricao', 'endereco', 'contato', 'status',)

    # included_serializers = {
    #     "endereco": "demandas.serializers.EnderecoSerializer",
    #     "contato": "demandas.serializers.ContatoSerializer",
    # }