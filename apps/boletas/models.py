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

    @staticmethod
    def get_boletas_operador(usuario):
        try:
            boletas = Boleta.objects.filter(cedula_empleado=usuario.cedula, reserva=False)
            return boletas
        except Sala.DoesNotExist and Funcion.DoesNotExist:
            return None

    @staticmethod
    def get_boletas_sucursal(usuario):
        try:
            boletas = Boleta.objects.filter(funcion__sala__sucursal=Empleado.objects.get(user=usuario).sucursal, reserva=False)
            return boletas
        except Sala.DoesNotExist and Funcion.DoesNotExist:
            return None

    def get_boletas():
        try:
            boletas = Boleta.objects.filter(reserva=False)
            return boletas
        except Funcion.DoesNotExist:
            return None





