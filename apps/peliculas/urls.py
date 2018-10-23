from django.urls import path , include
from apps.peliculas.views import *

app_name = 'peliculas'

urlpatterns = [

    path('crear/', crearPelicula, name='crear'),
    path('editar/<int:id_pelicula>', editar_pelicula, name='editar_pelicula'),

]