from django.urls import path
from apps.boletas.views import *

app_name = 'boletas'

urlpatterns = [
    path('vender-boleta', vender_boleta, name='vender_boleta'),
    path('api/consultar-pelicula', consultar_pelicula, name='consultar_pelicula'),
    path('api/consultar-funciones', consultar_funciones, name='consultar_funciones'),
    path('api/consultar-sala', consultar_sala, name='consultar_sala'),
]