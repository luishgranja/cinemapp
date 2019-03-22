from django.shortcuts import render
from apps.boletas.forms import *
from apps.peliculas.models import *
from apps.funciones.models import *
from apps.salas.models import *
from django.http.response import JsonResponse
from django.contrib import messages


def vender_boleta(request):
    usuario = request.user
    peliculas = Pelicula.get_pelicula_estreno(True)

    if request.method == 'POST':
        lista_sillas = request.POST.get('boletas', None)
        id_funcion = request.POST.get('funcion', None)
        funcion = Funcion.objects.get(id=id_funcion)
        sillas = eval(lista_sillas)
        flag_error = False;
        for silla in sillas:
            i = silla['i']
            j = silla['j']
            tipo = silla['color']
            silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
            boleta_funcion = Boleta.objects.filter(funcion=funcion, silla=silla_aux)
            if(boleta_funcion.count() != 0):
                flag_error = true

        if flag_error:
            messages.error(request, 'Hay algunas sillas que no estan disponibles')

        form = CrearBoletaForm(request.POST)
        if form.is_valid() and not(flag_error):
            for silla in sillas:
                i = silla['i']
                j = silla['j']
                tipo = silla['color']
                silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
                boleta_aux = Boleta()
                boleta_aux.total = 3800 #CORREGIR PRECIO BOLETA ESTOY AQUI NO ME IGNOREN
                boleta_aux.funcion = funcion
                boleta_aux.silla = silla_aux
                boleta_aux.cedula = form.data["cedula"]
                boleta_aux.cedula_empleado = usuario.cedula
                boleta_aux.nombre_cliente = form.data["nombre_cliente"]
                boleta_aux.save()

            messages.success(request, 'Boleta registrada exitosamente!')
            return render(request, 'boletas/vender_boleta.html', {'form': form, 'itemlist': list(range(0,26)), 'lista_sillas': 'lista_sillas', 'peliculas': peliculas,
                                                              'form_saldo': SaldoForm()})
        else:
            boletas_compradas = Boleta.objects.filter(funcion=funcion)
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'boletas/vender_boleta.html',
                          {'form': form, 'itemlist': list(range(0, 26)), 'lista_sillas': 'lista_sillas',
                           'peliculas': peliculas,
                           'form_saldo': SaldoForm()})
    else:
        form = CrearBoletaForm()
        return render(request, 'boletas/vender_boleta.html', {'form': form, 'itemlist': list(range(0,26)), 'lista_sillas': 'lista_sillas', 'peliculas': peliculas,
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


def consultar_boletas_funcion(request):
    if request.is_ajax():
        funcion_id = request.GET.get('funcion_id', None)
        try:
            funcion = Funcion.objects.get(id=int(funcion_id))
            boletas_fumcion = Boleta.objects.filter(funcion=funcion)
            print(boletas_fumcion)
            boletas_json = []
            for boleta in boletas_fumcion:
                boleta_json = {"i": boleta.silla.ubicacion_x, "j": boleta.silla.ubicacion_y}
                boletas_json.append(boleta_json)
            return JsonResponse({'boletas_funcion': boletas_json})

        except Funcion.DoesNotExist:
            return JsonResponse({'response': 0})
