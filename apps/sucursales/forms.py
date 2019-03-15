from apps.sucursales.models import *
from django_select2.forms import Select2Widget, ModelSelect2Widget
from django import forms
import re


class CreateSurcursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = ('nombre', 'telefono', 'direccion', 'is_active')
        labels = {
            'is_active': 'Activo'

        }

    def __init__(self, *args, **kwargs):
        super(CreateSurcursalForm, self).__init__(*args, **kwargs)

        for fieldname in ['nombre', 'telefono', 'direccion', 'is_active']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = ''

    def clean(self):
        nombre = self.cleaned_data['nombre']
        direccion = self.cleaned_data['direccion']
        telefono = self.cleaned_data['telefono']

        regex_nombre = re.compile('^[a-zA-ZÀ,.\s]{3,20}$', re.IGNORECASE)
        regex_direccion = re.compile('^[-%&+# \w]{6,50}$', re.IGNORECASE)
        regex_telefono = re.compile('^[0-9]{7,11}$')

        if not regex_nombre.match(nombre):
            self.add_error('nombre','Nombre debe ser mayor a 3 caracteres y a-z')

        if not regex_direccion.match(direccion):
            self.add_error('direccion','Dirección debe ser mayor a 6 caracteres')

        if not regex_telefono.match(telefono):
            self.add_error('telefono','Teléfono deber ser entre 7 y 11 números')

        return self.cleaned_data


class EditarSucursalForm(forms.ModelForm):
    gerente = forms.CharField(widget=ModelSelect2Widget(
        model=Empleado,
        search_fields=['user__first_name__icontains'],
        queryset=Empleado.objects.filter(cargo='Gerente').filter(sucursal_id=None)
    ), required=False)

    class Meta:
        model = Sucursal
        fields = ('nombre', 'telefono', 'direccion', 'is_active',)
        labels = {
            'is_active': 'Activo'

        }

    def clean(self):
        nombre = self.cleaned_data['nombre']
        direccion = self.cleaned_data['direccion']
        telefono = self.cleaned_data['telefono']

        regex_nombre = re.compile('^[a-zA-ZÀ ,.]{3,20}$', re.IGNORECASE)
        regex_direccion = re.compile('^[%&+ \w]{6,50}$', re.IGNORECASE)
        regex_telefono = re.compile('^[0-9]{7,11}$')

        if not regex_nombre.match(nombre):
            self.add_error('nombre','Nombre debe ser mayor a 3 caracteres y a-z')

        if not regex_direccion.match(direccion):
            self.add_error('last_name','Dirección debe ser mayor a 6 caracteres')

        if not regex_telefono.match(telefono):
            self.add_error('telefono','Teléfono deber ser entre 7 y 11 números')

        return self.cleaned_data

