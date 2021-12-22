from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from demandas.models import Demanda, Endereco, Contato
from demandas.serializers import DemandaSerializer

class DemandaViewSet(viewsets.ModelViewSet):
    '''CRUD de demanda'''
    permission_classes = (IsAuthenticated, )
    serializer_class = DemandaSerializer

    def get_queryset(self):
        print(self.request.user)
        demandas = Demanda.objects.all()
        return demandas
    
    def create(self, request, *args, **kwargs):
        print(request.user)
        print(request.user.id)
        demanda_data = request.data
        print('demanda_data')
        print(demanda_data)

        new_endereco = Endereco.objects.create(
            estado = demanda_data['endereco']['estado'],
            cidade = demanda_data['endereco']['cidade'],
            endereco = demanda_data['endereco']['endereco'],
            numero = demanda_data['endereco']['numero'],
        )
        new_endereco.save()
        print(new_endereco)
        new_contato = Contato.objects.create(
            email = demanda_data['contato']['email'],
            telefone = demanda_data['contato']['telefone'],
        )
        new_contato.save()
        print(new_contato)
        new_demanda = Demanda.objects.create(
            descricao = demanda_data['descricao'],
            endereco = new_endereco,
            contato = new_contato,
            anunciante = request.user,
            status = demanda_data['status']
        )
        print(new_demanda)
        serializer = DemandaSerializer(new_demanda)
        return Response(serializer.data)

