from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUsuario
from accounts.serializers import UsuarioSerializer

class UsuarioCreateAPIView(CreateAPIView):
    '''CRUD de usuário'''
    queryset = CustomUsuario.objects.all()
    serializer_class = UsuarioSerializer