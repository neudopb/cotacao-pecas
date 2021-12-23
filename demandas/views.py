from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from demandas.models import Demanda, Endereco, Contato
from accounts.models import CustomUsuario
from demandas.serializers import DemandaSerializer
from django.http import HttpResponse


class DemandaViewSet(CreateAPIView, ListAPIView):
    '''Create e List demanda'''
    permission_classes = (IsAuthenticated, )
    serializer_class = DemandaSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            return Demanda.objects.all()
        else:
            return Demanda.objects.filter(anunciante=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        
        demanda_data = request.data

        if 'fechada' in demanda_data['status'].lower() or "baseline-highlight_off.svg" == demanda_data['status']:
            demanda_data['status'] = "baseline-highlight_off.svg"
        else:
            demanda_data['status'] = "baseline-check_circle_outline.svg"

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

class DemandaUpdate(GenericAPIView, UpdateModelMixin):
    '''Update de demanda'''
    queryset = Demanda.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DemandaSerializer

    def put(self, request, *args, **kwargs):
        demanda_data = request.data
        get_demanda = Demanda.objects.get(id=kwargs.get('pk'))

        if self.request.user.id != get_demanda.anunciante.id and self.request.user.is_superuser == False:
            return HttpResponse('Unauthorized', status=401)
        
        get_demanda.endereco = demanda_data.get('endereco', get_demanda.endereco)
        get_demanda.status = demanda_data.get('status', get_demanda.status)

        if demanda_data.get('contato'):
            contato = Contato.objects.get(id=get_demanda.contato.id)
            contato.email = demanda_data['contato'].get('email', contato.email)
            contato.telefone = demanda_data['contato'].get('telefone', contato.telefone)
            contato.save()

        if demanda_data.get('endereco'):
            endereco = Endereco.objects.get(id=get_demanda.endereco.id)
            endereco.estado = demanda_data['endereco'].get('estado', endereco.estado)
            endereco.cidade = demanda_data['endereco'].get('cidade', endereco.cidade)
            endereco.endereco = demanda_data['endereco'].get('endereco', endereco.endereco)
            endereco.numero = demanda_data['endereco'].get('numero', endereco.numero)
            endereco.save()        

        get_demanda.save()
        return HttpResponse(status=204)

class DemandaDelete(GenericAPIView, DestroyModelMixin):
    '''Delete de demanda'''
    queryset = Demanda.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DemandaSerializer

    def delete(self, request, *args, **kwargs):
        demanda = self.get_object()

        if self.request.user.id != demanda.anunciante.id and self.request.user.is_superuser == False:
            return HttpResponse('Unauthorized', status=401)

        try:
            Contato.objects.filter(id=demanda.contato.id).delete()
        except: pass

        try:
            Endereco.objects.filter(id=demanda.endereco.id).delete()
        except: pass

        self.perform_destroy(demanda)

        return HttpResponse(status=204) 

class FinalizarDemanda(ListAPIView):
    '''Finalizar demanda'''
    queryset = Demanda.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DemandaSerializer

    def get_queryset(self):
        get_demanda = Demanda.objects.get(id=self.kwargs['pk'])
       
        if self.request.user.id == get_demanda.anunciante.id or self.request.user.is_superuser == True:
            get_demanda.status = "baseline-highlight_off.svg"  
            get_demanda.save()
        
        return Demanda.objects.filter(id=get_demanda.id)