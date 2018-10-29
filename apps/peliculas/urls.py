from django.urls import path
from apps.peliculas.views import *


app_name = 'peliculas'

urlpatterns = [

    path('gestion-peliculas', crear_pelicula, name='crear'),
    path('editar/<int:id_pelicula>', editar_pelicula, name='editar_pelicula'),
    path('ver-estrenos', consultar_peliculas, name='consultar_peliculas'),
    path('ver/<slug:slug>', ver_pelicula, name='ver_pelicula'),
    path('gestion-generos', crear_genero, name= 'crear_genero'),

]