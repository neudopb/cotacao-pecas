from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UsuarioCreateAPIView, UsuarioListAPIView
from demandas.views import DemandaViewSet, DemandaUpdate

router = routers.DefaultRouter()

router.register(r'demanda', DemandaViewSet, basename="demandas")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),

    path('usuario/', UsuarioCreateAPIView.as_view()),
    path('usuario/list', UsuarioListAPIView.as_view()),
    path('demanda/update/<int:pk>/', DemandaUpdate.as_view()),
    
]
