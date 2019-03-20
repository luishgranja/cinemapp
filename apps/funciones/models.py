from django.db import models
from apps.salas.models import Silla

# Create your models here.
class Funcion(models.Model):
	sala = models.ForeignKey('salas.Sala', on_delete=models.CASCADE)
	pelicula = models.ForeignKey('peliculas.Pelicula', on_delete=models.CASCADE)
	fecha_funcion = models.DateTimeField()
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

class PrecioFuncion(models.Model):
	funcion = models.ForeignKey('funciones.Funcion',on_delete=models.CASCADE,related_name="precios")
	tipo_silla= models.CharField(max_length=200,choices=Silla.TIPOS)
	precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	class Meta:
		unique_together = (('funcion', 'tipo_silla'),)



