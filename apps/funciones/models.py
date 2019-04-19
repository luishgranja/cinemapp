from django.db import models
from apps.salas.models import *
from apps.accounts.models import *
from datetime import date, timedelta


class Funcion(models.Model):
    sala = models.ForeignKey('salas.Sala', on_delete=models.CASCADE)
    pelicula = models.ForeignKey('peliculas.Pelicula', on_delete=models.CASCADE)
    fecha_funcion = models.DateField()
    hora_funcion = models.TimeField()

    @staticmethod
    def get_funciones_sucursales(usuario):
        try:
            salas = Sala.objects.filter(sucursal=Empleado.objects.get(user=usuario).sucursal)
            funciones = Funcion.objects.filter(sala__in=salas)
            return funciones
        except Sala.DoesNotExist and Funcion.DoesNotExist:
            return None

    def get_funciones():
        try:
            funciones = Funcion.objects.all()
            return funciones
        except Funcion.DoesNotExist:
            return None

    def get_funciones_actuales(usuario):
        fecha_actual = date.today()
        try:
            salas = Sala.objects.filter(sucursal=Empleado.objects.get(user=usuario).sucursal)
            funciones = Funcion.objects.filter(fecha_funcion__range=(fecha_actual, fecha_actual +
                                                                     timedelta(days=15)), sala__in=salas)
            return funciones
        except Funcion.DoesNotExist:
            return None

    def get_funcion(slug):
        return Funcion.objects.get(slug=slug)

    class Meta:
        ordering = ['sala__sucursal', 'fecha_funcion']
