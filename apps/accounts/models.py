from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def get_cargo_empleado(self):
        if self.is_staff:
            return 'Administrador'
        else:
            id_empleado = self.id
            cargo = Empleado.get_cargo(id_empleado)
            return cargo


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cliente')
    saldo = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    tarjeta = models.CharField(max_length=16)

    def __str__(self):
        return self.user.get_full_name()


class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='empleado')
    cargos = (('Gerente', 'Gerente'), ('Operador', 'Operador'))
    cargo = models.CharField(max_length=9, choices=cargos)
    sucursal = models.ForeignKey('sucursales.Sucursal', related_name='empleados', on_delete=models.CASCADE, blank=True,
                                 null=True)

    def __str__(self):
        return self.user.get_full_name()

    @staticmethod
    def get_info():
        try:
            empleados = Empleado.objects.all()
            return empleados
        except User.DoesNotExist:
            return None

    def get_gerente(id_sucursal):
        try:
            gerente = Empleado.objects.filter(cargo='Gerente').get(sucursal_id=id_sucursal)
            return gerente.user.get_full_name()
        except Empleado.DoesNotExist:
            return ''

    def listar_gerentes(self):
        try:
            gerentes = Empleado.objects.filter(cargo='Gerente').all()
            return gerentes
        except Empleado.DoesNotExist:
            return None

    def get_cargo(id_empleado):
        cargo_empleado = Empleado.objects.get(user_id=id_empleado).cargo
        if cargo_empleado == 'Gerente':
            return 'Gerente'
        else:
            return 'Operador'
