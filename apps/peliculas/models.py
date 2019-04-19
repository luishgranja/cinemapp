from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe


class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    @staticmethod
    def get_generos():
        try:
            generos = Genero.objects.all()
            return generos
        except Genero.DoesNotExist:
            return None

    def get_genero(id_genero):
        return Genero.objects.get(id=id_genero)


class Pelicula(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    nombre_director = models.CharField(max_length=20)
    genero = models.ManyToManyField(Genero, blank=True)
    sinopsis = models.TextField(max_length=300)
    reparto = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    imagen = models.ImageField(upload_to='peliculas/', null=True, blank=True, default='/peliculas/default.jpg')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, default='')
    is_estreno = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def save(self, *args):
        self.slug = slugify(self.nombre)
        super(Pelicula, self).save(*args)

    @staticmethod
    def get_peliculas():
        try:
            peliculas = Pelicula.objects.all()
            return peliculas
        except Pelicula.DoesNotExist:
            return None

    def get_pelicula(slug):
        return Pelicula.objects.get(slug=slug)

    def get_peliculas_activas():
        try:
            peliculas = Pelicula.objects.filter(is_active=True)
            return peliculas
        except Pelicula.DoesNotExist:
            return None

    def get_pelicula_estreno(opcion):
        try:
            peliculas = Pelicula.objects.filter(is_estreno=opcion)
            return peliculas
        except Pelicula.DoesNotExist:
            return None
