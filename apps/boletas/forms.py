from django import forms
from apps.boletas.models import *


class CrearBoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ('funcion', 'cedula', 'nombre_cliente', 'medio_pago')
