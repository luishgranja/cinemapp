from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import Empleado


class SignUpForm(UserCreationForm):
    class Meta:
        model = Empleado
        fields = ('first_name', 'last_name', 'cedula_empleado', 'username', 'email', 'password1', 'password2', 'cargo',
                  'sucursal', 'is_active')