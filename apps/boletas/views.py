from django.shortcuts import render
from apps.boletas.forms import *
from apps.peliculas.models import *
from apps.funciones.models import *
from django.http.response import JsonResponse


def vender_boleta(request):
    usuario = request.user
    peliculas = Pelicula.get_pelicula_estreno(True)

    if request.method == 'GET':
        form = CrearBoletaForm()
        return render(request, 'boletas/vender_boleta.html', {'form': form, 'peliculas': peliculas,
                                                              'form_saldo': SaldoForm()})


def consultar_pelicula(request):
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            return JsonResponse({'sinopsis': pelicula.sinopsis})
        except Pelicula.DoesNotExist:
            return JsonResponse({'response': 0})

def consultar_funcion(request):
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            funciones = Funcion.objects.filter(pelicula=pelicula)
            lista_funciones = []
            for funcion in lista_funciones:
                id_funcion = funcion.id
                lista_funciones.append({'id':funcion.id, 'fecha': funcion.fecha_funcion, 'hora': funcion.hora_funcion})

            return JsonResponse({'lista_funciones': lista_funciones})
        except Pelicula.DoesNotExist:
            return JsonResponse({'response': 0})
