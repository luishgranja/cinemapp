from django.urls import path , include
from apps.sucursales.views import *
from django.contrib.auth import views as auth_views

app_name = 'sucursales'

urlpatterns = [

    path('crear/', createSucursal, name='crear'),
    path('editar/<int:id_sucursal>', editar_sucursal, name='editar_sucursal'),

]