from django import forms
from django_select2.forms import ModelSelect2Widget
from django_select2.forms import Select2Widget
from apps.salas.models import *
from apps.funciones.models import *
from apps.sucursales.models import *


class CrearFuncionForm(forms.ModelForm):

    def listarSalas(self,id_sucursal):
        sala = forms.CharField(widget=ModelSelect2Widget(
            model=Sala,
            search_fields=['user__first_name__icontains'],
            queryset=Sala.objects.filter(sucursal=Sucursal.objects.get(id=id_sucursal))
        ), required=False)
        self.fields['sala'] = sala

    class Meta:
        model = Funcion
        fields = ('sala', 'pelicula', 'fecha_funcion','hora_funcion')

        widgets = {
            'pelicula': Select2Widget(),
            'hora_funcion': forms.TimeInput(format='%H:%M')
        }

