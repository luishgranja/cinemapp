from django.db import models
from apps.salas.models import Silla


class Funcion(models.Model):
	sala = models.ForeignKey('salas.Sala', on_delete=models.CASCADE)
	pelicula = models.ForeignKey('peliculas.Pelicula', on_delete=models.CASCADE)
	fecha_funcion = models.DateField()
	hora_funcion =models.TimeField()
	@staticmethod
	def get_funciones():
		try:
			funciones = Funcion.objects.all()
			return funciones
		except Funcion.DoesNotExist:
			return None

	def get_funcion(slug):
		return Funcion.objects.get(slug=slug)


