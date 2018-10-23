from apps.sucursales.models import *
from django_select2.forms import Select2Widget, ModelSelect2Widget
from django import forms


class CreateSurcursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = ('nombre', 'telefono', 'direccion', 'is_active')
        labels = {
            'is_active': 'Activo'

        }


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

