from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf.urls.static import static
from django.conf import settings

from accounts.views import UsuarioCreateAPIView, UsuarioListAPIView
from demandas.views import DemandaViewSet, DemandaUpdate, DemandaDelete, FinalizarDemanda


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('usuario/', UsuarioCreateAPIView.as_view()),
    path('usuario/list', UsuarioListAPIView.as_view()),
    path('demanda/', DemandaViewSet.as_view()),
    path('demanda/update/<int:pk>/', DemandaUpdate.as_view()),
    path('demanda/delete/<int:pk>/', DemandaDelete.as_view()),
    path('demanda/finalizar/<int:pk>/', FinalizarDemanda.as_view()),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
