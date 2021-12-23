from rest_framework import serializers
from accounts.models import CustomUsuario
from django.contrib.auth.hashers import make_password

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsuario
        fields = ['id', 'first_name', 'email', 'password', 'is_superuser']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['username'] = validated_data['email']
        return super(UsuarioSerializer, self).create(validated_data)

class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsuario
        fields = ['id', 'first_name', 'email', 'is_superuser']
