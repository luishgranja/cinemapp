from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import *


class CrearFuncionForm(forms.ModelForm):
    class Meta:
        model = Funcion
        fields = ('sala', 'pelicula', 'fecha_funcion','hora_funcion')

