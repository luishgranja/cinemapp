from django.urls import path
from apps.boletas.views import *

app_name = 'boletas'

urlpatterns = [
    path('comprar-boleta', comprar_boleta, name='comprar_boleta'),
    path('api/consultar-pelicula', consultar_pelicula, name='consultar_pelicula'),
]