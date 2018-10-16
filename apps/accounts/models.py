from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.sucursales.models import Sucursal


class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    telefono = models.CharField(max_length=11)
    cedula = models.CharField(max_length=11, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cedula', 'email', 'is_active', 'cargo', 'telefono',
                       'is_cliente']
    USERNAME_FIELD = 'username'

    @staticmethod
    def get_empleados():
        try:
            empleados = User.objects.filter(is_cliente=False)
            return empleados
        except User.DoesNotExist:
            return None



class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cliente')
    saldo = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    tarjeta = models.CharField(max_length=16)


class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='empleado')
    cargos = (('Gerente', 'Gerente'), ('Operador', 'Operador'))
    cargo = models.CharField(max_length=9, choices=cargos)
    sucursal = models.ForeignKey(Sucursal, related_name='empleados', on_delete=models.CASCADE, blank=True,
                                 null=True)

    @staticmethod
    def get_info():
        try:
            empleados = Empleado.objects.all()
            return empleados
        except User.DoesNotExist:
            return None