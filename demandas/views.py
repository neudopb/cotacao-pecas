from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from demandas.models import Demanda, Endereco, Contato
from accounts.models import CustomUsuario
from demandas.serializers import DemandaSerializer

class DemandaViewSet(viewsets.ModelViewSet):
    '''CRUD de demanda'''
    permission_classes = (IsAuthenticated, )
    serializer_class = DemandaSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            return Demanda.objects.all()
        else:
            return Demanda.objects.filter(anunciante=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        
        demanda_data = request.data

        new_endereco = Endereco.objects.create(
            estado = demanda_data['endereco']['estado'],
            cidade = demanda_data['endereco']['cidade'],
            endereco = demanda_data['endereco']['endereco'],
            numero = demanda_data['endereco']['numero'],
        )
        new_endereco.save()
        
        new_contato = Contato.objects.create(
            email = demanda_data['contato']['email'],
            telefone = demanda_data['contato']['telefone'],
        )
        new_contato.save()
        
        
        if request.user.is_superuser == True and demanda_data.get('anunciante'):
            usuario = CustomUsuario.objects.filter(id=demanda_data.get('anunciante'))
            usuario = usuario and usuario[0] or request.user
        else:
            usuario = request.user

        
        new_demanda = Demanda.objects.create(
            descricao = demanda_data['descricao'],
            endereco = new_endereco,
            contato = new_contato,
            anunciante = usuario,
            status = demanda_data['status']
        )

        serializer = DemandaSerializer(new_demanda)
        return Response(serializer.data)

