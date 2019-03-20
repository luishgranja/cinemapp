from django.urls import path
from apps.salas.views import *


app_name = 'salas'

urlpatterns = [

    path('gestion-salas', crear_sala, name='crear'),
    path('editar/<int:id_sala>', editar_sala, name='editar_sala'),
    path('ver/<id_sala>', ver_sala, name='ver_sala'),



]