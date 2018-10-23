from django import forms
from .models import *


class CrearPeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ('nombre','nombre_director','genero','sinopsis','reparto','imagen')
