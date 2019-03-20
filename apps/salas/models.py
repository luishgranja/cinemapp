from django.db import models


# Create your models here.
class Sala(models.Model):
	SALA_4DX ="SALA_4DX"
	SALA_IMAX ="SALA_IMAX"
	MEGA_SALA ="MEGA_SALA"
	SALA_XD="SALA_XD"
	TIPOS =(
		(SALA_4DX,"Sala 4D"),
		(SALA_IMAX, "Sala IMAX"),
		(MEGA_SALA,"Mega Sala"),
		(SALA_XD,"Sala XD"),
	)

	tipo_sala = models.CharField(max_length=200,choices=TIPOS)
	num_sala = models.PositiveIntegerField()
	sucursal = models.ForeignKey('sucursales.Sucursal', on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	class Meta:
		unique_together = (('num_sala', 'sucursal'),)

	def __str__(self):
		aux=str(self.num_sala)+" - "+self.get_tipo_sala_display()
		return aux		

	@staticmethod
	def get_salas():
		try:
			salas = Sala.objects.all()
			return salas
		except Sala.DoesNotExist:
			return None

	def get_salas_de_sucursal(id):
		try:
			salas = Sala.objects.filter(sucursal_id=id)
			return salas
		except Sala.DoesNotExist:
			return None

	def get_sala(id):
		return Sala.objects.get(id=id)

class Silla(models.Model):
	PREFERENCIAL ="PREFERENCIAL"
	GENERAL ="GENERAL"
	DISCAPACITADO ="DISCAPACITADO"
	TIPOS =(
		(PREFERENCIAL,"Preferencial"),
		(GENERAL, "General"),
		(DISCAPACITADO,"Discapacitado"),
	)
	nombre = models.CharField(max_length=255)
	tipo= models.CharField(max_length=200,choices=TIPOS)
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

	


