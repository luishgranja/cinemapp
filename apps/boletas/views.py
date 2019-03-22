from django.shortcuts import render
from apps.boletas.forms import *
from apps.peliculas.models import *
from apps.funciones.models import *
from apps.salas.models import *
from django.http.response import JsonResponse


def vender_boleta(request):
    usuario = request.user
    peliculas = Pelicula.get_pelicula_estreno(True)
    lista_sillas=request.POST.getlist('silla')

    if request.method == 'GET':
        form = CrearBoletaForm()
        return render(request, 'boletas/vender_boleta.html', {'form': form, 'itemlist': list(range(0,26)), 'lista_sillas': lista_sillas, 'peliculas': peliculas,
                                                              'form_saldo': SaldoForm()})


def consultar_pelicula(request):
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            return JsonResponse({'sinopsis': pelicula.sinopsis})
        except Pelicula.DoesNotExist:
            return JsonResponse({'response': 0})


def consultar_funciones(request):
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            funciones = Funcion.objects.filter(pelicula=pelicula)
            lista_funciones = []
            for funcion in funciones:
                lista_funciones.append({'id': funcion.id, 'fecha': funcion.fecha_funcion, 'hora': funcion.hora_funcion})
            return JsonResponse({'lista_funciones': lista_funciones})
        except Pelicula.DoesNotExist:
            return JsonResponse({'response': 0})


def get_color_silla(tipo):
    if tipo == 'PREFERENCIAL':
        return 'background: rgb(255, 91, 185 );'
    elif tipo == 'GENERAL':
        return 'background: rgb(255, 91, 185 );'
    elif tipo == 'DISCAPACITADO':
        return 'background: rgb(0, 185, 240);'
    else:
        return 'background: rgb(223, 214, 223);'


def consultar_sala(request):
    if request.is_ajax():
        funcion_id = request.GET.get('funcion_id', None)
        try:
            funcion = Funcion.objects.get(id=funcion_id)
            sala = Sala.objects.get(funcion=funcion)
            sillas = sala.sillas.all()
            lista_sillas = []
            for i in range(0, 677):
                lista_sillas.append(False)

            for silla in sillas:
                silla_numero = (26 * (silla.ubicacion_x + 1 - 1)) + silla.ubicacion_y + 1
                lista_sillas[silla_numero] = silla

            html = ""

            for i in range(0, 26):
                html += '<div class="flex-container">'
                for j in range(0, 26):
                    pos = (i*26)+j+1
                    silla = lista_sillas[pos]
                    if silla:
                        html += "<div> <input id='"+str(i)+"-"+str(j)+"' class='"+silla.tipo+"' onclick='myFunction(this)' type='checkbox'  name='silla' hola='"+silla.nombre+"' checked value=" + "{'i':" +str(i)+",'j':" +str(j)+",'color':'" + silla.tipo+"'}> </div>"
                    else:
                        html += '<div> <input id="'+str(i)+'-'+str(j)+'" class="SIN_MARCAR" onclick="myFunction(this)" type="checkbox" name="silla" value="{"i":"'+str(i)+',"j":'+str(j)+',"color": "SIN_MARCAR"}" disabled=""> </div>'

                html += '</div>'
            return JsonResponse({'html': html})

        except Funcion.DoesNotExist:
            return JsonResponse({'response': 0})
