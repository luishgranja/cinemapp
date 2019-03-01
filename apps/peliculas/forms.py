from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import *
import re


class CrearPeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ('nombre', 'nombre_director', 'genero', 'sinopsis', 'reparto', 'imagen', 'is_active', 'is_estreno', )
        widgets = {
            'genero': Select2MultipleWidget(),
            'sinopsis': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'is_active': 'Activo',
            'is_estreno': '¿La película esta en estreno?'
        }
        # help_texts = {
         #   'reparto': 'Por favor escribir los nombres de los actores separados por una coma (,) \n Ej: Emilia Clarke, '
          #             'Peter Dinklage, Sophie Turner, ...',
           # 'imagen': 'Por favor seleccione una imagen.',
            #'sinopsis': 'Escriba un resumen muy breve y general de la pelicula.',
            #'is_estreno': 'Seleccione la opción si la pelicula se encuentra en estreno.'
        #}

    def clean(self):
        nombre = self.cleaned_data['nombre']
        director = self.cleaned_data['nombre_director']
        sinopsis = self.cleaned_data['sinopsis']
        reparto = self.cleaned_data['reparto']
        genero = self.cleaned_data['genero']

        regex_director = re.compile('^[a-zA-ZÀ, ]{3,30}$', re.IGNORECASE)
        regex_reparto = re.compile('^[a-zA-ZÀ, ]{3,300}$', re.IGNORECASE)

        if not len(nombre):
            self.add_error('nombre','Nombre debe ser mayor a 3 caracteres y a-z')

        if not regex_director.match(director):
            self.add_error('nombre_director','Aqui error debe ser mayor a 3 caracteres y a-z')

        if not len(sinopsis):
            self.add_error('sinopsis','Sinopsis debe ser mayor a 3 caracteres y a-z')

        if not regex_reparto.match(reparto):
            self.add_error('reparto','Reparto debe ser mayor a 3 caracteres y a-z')

        try:
            g = Genero.objects.filter(nombre=genero)
        except Genero.DoesNotExist:
            self.add_error('genero', 'Género no registrado')

        return self.cleaned_data



class CrearGeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('nombre',)


    def clean(self):
        nombre = self.cleaned_data['nombre']

        regex = re.compile('^[a-z]{4,20}$', re.IGNORECASE)

        if not regex.match(nombre):
            self.add_error('nombre', 'El género debe ser mayor a 5 caracteres y a-z')

        return self.cleaned_data

