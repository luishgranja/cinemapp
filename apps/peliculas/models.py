from django.db import models

# Create your models here.

class ImagenPelicula(models.Model):
    imagen = models.ImageField(upload_to = 'peliculas/')

    def __str__(self):
        return self.imagen.url

class Pelicula(models.Model):
    nombre = models.CharField(max_length=50)
    nombre_director = models.CharField(max_length=20)
    GENEROS = (
        ('a', 'Hola'),
        ('b', 'Hello'),
        ('c', 'Bonjour'),
        ('d', 'Boas'),
    )
    genero = models.CharField(max_length=15, choices=GENEROS)
    sinopsis = models.TextField(max_length=300)
    reparto = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    imagen = models.OneToOneField(ImagenPelicula, blank=True, on_delete=models.CASCADE)


