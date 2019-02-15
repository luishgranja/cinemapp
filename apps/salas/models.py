from django.db import models


# Create your models here.
class Sala(models.Model):

	tipo_sala = models.CharField(max_length=255)
	num_sala = models.IntegerField()
	sucursal = models.ForeignKey('sucursales.Sucursal', on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	class Meta:
		unique_together = (('num_sala', 'sucursal'),)

	@staticmethod
	def get_salas():
		try:
			salas = Sala.objects.all()
			return salas
		except Sala.DoesNotExist:
			return None

	def get_sala(id):
		return Sala.objects.get(id=id)


class Silla(models.Model):
	nombre = models.CharField(max_length=255)
	sala = models.ForeignKey('salas.Sala',on_delete=models.CASCADE,related_name='sillas')
	ubicacion_x= models.IntegerField()
	ubicacion_y= models.IntegerField()

	@staticmethod
	def get_sillas():
		try:
			salas = Sala.objects.all()
			return salas
		except Sala.DoesNotExist:
			return None

	def get_sala(slug):
		return Sala.objects.get(slug=slug)

	


