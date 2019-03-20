from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import *


class CrearSalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ('tipo_sala', 'num_sala', 'sucursal','is_active')
        labels = {
            'is_active': 'Activo',
        }

