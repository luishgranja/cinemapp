from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import *


class CrearPeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ('nombre', 'nombre_director', 'genero', 'sinopsis', 'reparto', 'imagen', 'is_active', 'is_estreno')
        widgets = {
            'genero': Select2MultipleWidget(),
            'sinopsis': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'is_active': 'Activo',
            'is_estreno': '¿La película esta en estreno?'
        }
        help_texts = {
            'reparto': 'Por favor escribir los nombres de los actores separados por una coma (,) \n Ej: Emilia Clarke, '
                       'Peter Dinklage, Sophie Turner, ...',
            'imagen': 'Por favor seleccione una imagen.',
            'sinopsis': 'Escriba un resumen muy breve y general de la pelicula.',
            'is_estreno': 'Seleccione la opción si la pelicula se encuentra en estreno.'
        }


class CrearGeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('nombre',)
        help_texts = {
            'nombre': 'Ingrese el nombre de un genero cinematográfico.'
        }

