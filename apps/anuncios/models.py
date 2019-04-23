from django.db import models


# Create your models here.
class Anuncio(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='anuncios/', null=True, blank=True, default='/anuncios/default.jpg')
    descripcion = models.TextField(max_length=300)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    UBICACION_ANUNCIO_LIST = (
        ('compra_boletas', 'Compra de Boletas'),
        ('reserva_boletas', 'Reserva de Boletas'),
        ('dashboard', 'Pantalla de Inicio'),
    )
    ubicacion_anuncio = models.CharField(choices=UBICACION_ANUNCIO_LIST, max_length=20)
