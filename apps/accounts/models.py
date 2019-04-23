from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    telefono = models.CharField(max_length=11)
    cedula = models.CharField(max_length=11, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cedula', 'email', 'is_active', 'cargo', 'telefono',
                       'is_cliente']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.cedula + ' - ' + self.get_full_name()

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
            cargo = Empleado.get_cargo(self.id)
            return cargo

    def get_clientes():
        try:
            clientes = User.objects.filter(is_cliente=True)
            return clientes
        except User.DoesNotExist:
            return None


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cliente')
    saldo = models.IntegerField(default=0)

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


class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notificaciones')
    titulo = models.CharField(max_length=120, blank=True)
    mensaje = models.TextField(max_length=350)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    # 1:warning 2:error 3:compras 4:promociones 5:peliculas
    tipo = models.CharField(max_length=2)

    def get_icono(self):
        opciones = {
            '1': 'fa fa-exclamation-triangle text-yellow',
            '2': 'fa fa-exclamation-circle text-red',
            '3': 'fa fa-shopping-cart text-green',
            '4': 'fa fa-tags text-maroon',
            '5': 'fa fa-video-camera text-purple'
        }
        return opciones[self.tipo]

    class Meta:
        ordering = ['-fecha_envio']
