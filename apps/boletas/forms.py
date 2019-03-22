from django import forms
from apps.boletas.models import *
import re


class CrearBoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ('funcion', 'cedula', 'nombre_cliente', 'medio_pago')

    def __init__(self, *args, **kwargs):
        super(CrearBoletaForm, self).__init__(*args, **kwargs)

        for fieldname in ['cedula', 'nombre_cliente']:
            self.fields[fieldname].widget.attrs['placeholder'] = ''

    def clean(self):
        nombre = self.cleaned_data['nombre_cliente']
        cedula = self.cleaned_data['cedula']

        regex_nombre = re.compile('^[a-zA-ZÀ,\s]{3,20}$', re.IGNORECASE)
        regex_cedula = re.compile('^[0-9]{8,11}$')

        if not regex_nombre.match(nombre):
            self.add_error('nombre_cliente','Nombre debe ser mayor a 3 caracteres y a-z')

        if not regex_cedula.match(cedula):
            self.add_error('cedula','Cédula debe ser numérica entre 8 y 11 números')

        return self.cleaned_data


class SaldoForm(forms.Form):
    saldo_actual = forms.CharField(label='Saldo actual', widget=forms.TextInput(attrs={'disabled': True}))
    total_boleta = forms.CharField(label='Total a Pagar')

    def __init__(self, *args, **kwargs):
        super(SaldoForm, self).__init__(*args, **kwargs)

        for fieldname in ['saldo_actual', 'total_boleta']:
            self.fields[fieldname].widget.attrs['placeholder'] = ''