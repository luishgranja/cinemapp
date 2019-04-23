from django import forms
from django_select2.forms import Select2Widget
from apps.anuncios.models import *


class CrearAnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ('nombre', 'descripcion', 'imagen', 'ubicacion_anuncio', 'fecha_inicio', 'fecha_final')

        widgets = {
            'ubicacion_anuncio': Select2Widget(),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
