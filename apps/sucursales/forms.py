from django.contrib.auth.forms import UserCreationForm
from apps.sucursales.models import *
from django import forms

class createSurcursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ('nombre', 'telefono', 'direccion')