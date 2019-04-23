from django.urls import path
from apps.anuncios.views import *

app_name = 'anuncios'

urlpatterns = [
    path('gestion-anuncios', gestion_anuncios, name='gestion_anuncios'),
    path('editar/<int:id_anuncio>', editar_anuncio, name='editar_anuncio'),
    path('ver/<int:id_anuncio>', ver_anuncio, name='ver_anuncio'),
]
