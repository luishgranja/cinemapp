from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import *


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'cedula', 'username', 'email', 'password1', 'password2',
                  'telefono')


class SignUpFormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('tarjeta',)

class SignUpFormEmpleado(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ('cargo','sucursal')