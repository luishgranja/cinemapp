from django.db import models
from apps.funciones.models import *
from apps.salas.models import *


class Boleta(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    silla = models.ForeignKey(Silla, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=11, blank=False)
    cedula_empleado = models.CharField(max_length=11, blank=False)
    nombre_cliente = models.CharField(max_length=30, blank=False)
    fecha_compra = models.DateTimeField(auto_now=True)
    total = models.IntegerField(default=0, blank=False)
    reserva = models.BooleanField(default=False)

    MEDIOS_PAGO = (
        ('efectivo', 'Efectivo'),
        ('saldo', 'Saldo en cuenta'),
    )

    medio_pago = models.CharField(choices=MEDIOS_PAGO, default='efectivo', max_length=10)

    class Meta:
        ordering = ['-fecha_compra']





