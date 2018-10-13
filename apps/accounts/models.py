from django.db import models
from apps.sucursales.models import *
from django.contrib.auth.models import AbstractUser


class Cliente(AbstractUser):
    cedula = models.CharField(max_length=11, unique=True)
    saldo = models.DecimalField(max_digits=7, decimal_places=2)
    telefono = models.CharField(max_length=11)
    tarjeta = models.CharField(max_length=16)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cedula', 'email', 'username', 'is_active', 'saldo', 'telefono',
                       'tarjeta']
    USERNAME_FIELD = 'email'


class Empleado(AbstractUser):
    cedula_empleado = models.CharField(max_length=11, unique=True)
    telefono = models.CharField(max_length=11)
    cargos = (('gerente', 'Gerente'), ('operador', 'Operador'))
    cargo = models.CharField(choices=cargos)
    sucursal = models.ForeignKey(Sucursal, related_name='empleados', on_delete=models.CASCADE, blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cedula_empleado', 'email', 'username', 'is_active', 'cargo',
                       'telefono', 'sucursal']
    USERNAME_FIELD = 'cedula_empleado'
