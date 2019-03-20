from django.urls import path
from apps.funciones.views import *


app_name = 'funciones'

urlpatterns = [

    path('gestion-funciones', crear_funcion, name='crear'),
    
]