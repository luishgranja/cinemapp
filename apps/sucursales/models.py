from django.db import models
from apps.accounts.models import *


class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=11)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    @staticmethod
    def get_info():
        try:
            sucursales = Sucursal.objects.all()
            return sucursales
        except Sucursal.DoesNotExist:
            return None