from django.db import models
from apps.accounts.models import Empleado


class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    gerente = models.OneToOneField(Empleado, related_name='sucursales', on_delete=models.CASCADE, null=True)
    telefono = models.CharField(max_length=11)
    direccion = models.CharField(max_length=100)
