from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import *


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'cedula', 'username', 'email', 'password1', 'password2',
                  'telefono')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('tarjeta',)


class FormEmpleado(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ('cargo', 'sucursal')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'cedula', 'username', 'email', 'telefono', 'is_active')
