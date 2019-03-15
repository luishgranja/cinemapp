from django.shortcuts import render
from apps.boletas.forms import *
from apps.peliculas.models import *
from django.http.response import JsonResponse


def comprar_boleta(request):
    usuario = request.user
    peliculas = Pelicula.get_pelicula_estreno(True)

    if request.method == 'GET':
        form = CrearBoletaForm()
        return render(request, 'boletas/comprar_boleta.html', {'form': form, 'peliculas': peliculas})


def consultar_pelicula(request):
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            return JsonResponse({'sinopsis': pelicula.sinopsis})
        except Pelicula.DoesNotExist:
            return JsonResponse({'response': 0})

