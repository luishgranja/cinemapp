from django.db import models


class Boleta(models.Model):
    funcion = models.IntegerField()
    silla = models.IntegerField()
    cedula = models.CharField(max_length=11, blank=False)
    cedula_empleado = models.CharField(max_length=11, blank=False)
    nombre_cliente = models.CharField(max_length=30, blank=False)
    fecha_compra = models.DateTimeField(auto_now=True)
    total = models.IntegerField(default=0, blank=False)

    MEDIOS_PAGO = (
        ('efectivo', 'Efectivo'),
        ('saldo', 'Saldo en cuenta'),
    )

    medio_pago = models.CharField(choices=MEDIOS_PAGO, default='efectivo', max_length=10)





