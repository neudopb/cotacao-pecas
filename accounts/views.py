from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUsuario
from accounts.serializers import UsuarioSerializer, UsuarioListSerializer

class UsuarioCreateAPIView(CreateAPIView):
    '''Cadastrar usuário'''
    queryset = CustomUsuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioListAPIView(ListAPIView):
    '''Listar usuario'''
    permission_classes = (IsAuthenticated,)
    serializer_class = UsuarioListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            return CustomUsuario.objects.all()
        else:
            return CustomUsuario.objects.filter(email=self.request.user.email)