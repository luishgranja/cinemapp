from django.shortcuts import render, redirect
from apps.boletas.forms import *
from apps.peliculas.models import *
from apps.funciones.models import *
from apps.salas.models import *
from apps.accounts.models import *
from django.http.response import JsonResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from apps.accounts.models import *
from apps.boletas.utilities import generar_pdf_boleta
from django.http import HttpResponseNotFound


def generar_boleta(request, id_boleta):
    usuario = request.user
    boleta = get_object_or_404(Boleta, id=id_boleta)
    if boleta:
        return generar_pdf_boleta(boleta)

# Crear reserva para el Cliente
def crear_reserva(request, slug, id_funcion):
    usuario = request.user
    funcion = Funcion.objects.get(id=id_funcion)
    pelicula = Pelicula.objects.get(funcion=funcion)
    tipo_sala = funcion.sala.tipo_sala

    if request.method == 'POST':
        lista_sillas = request.POST.get('boletas', None)
        funcion = Funcion.objects.get(id=id_funcion)
        sillas = eval(lista_sillas)
        precio_final = request.POST.get('precio_final', None)
        flag_error = False
        for silla in sillas:
            i = silla['i']
            j = silla['j']
            tipo = silla['color']
            silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
            boleta_funcion = Boleta.objects.filter(funcion=funcion, silla=silla_aux)
            if boleta_funcion.count() != 0:
                flag_error = True

        if flag_error:
            messages.error(request, 'Hay algunas sillas que no están disponibles')

        form = CrearBoletaForm(request.POST)
        if form.is_valid() and not flag_error:
            if form.cleaned_data['medio_pago'] == 'saldo':
                saldo_actual = usuario.cliente.saldo
                if saldo_actual >= int(precio_final):
                    for silla in sillas:
                        i = silla['i']
                        j = silla['j']
                        silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
                        boleta_aux = Boleta()

                        # Calculo del precio boleta
                        tipo_silla = silla_aux.tipo

                        precio_silla = {
                            'GENERAL': 2000,
                            'PREFERENCIAL': 3000,
                            'DISCAPACITADO': 1000
                        }

                        precio_sala = {
                            "SALA_GENERAL": 4000,
                            "SALA_IMAX": 5000,
                            "SALA_3D": 4500,
                            "SALA_4DX": 6000
                        }

                        boleta_aux.total = precio_silla[tipo_silla] + precio_sala[funcion.sala.tipo_sala] + 2800
                        boleta_aux.funcion = funcion
                        boleta_aux.reserva = True
                        boleta_aux.silla = silla_aux
                        boleta_aux.cedula = form.data["cedula"]
                        boleta_aux.cedula_empleado = usuario.cedula
                        boleta_aux.nombre_cliente = form.data["nombre_cliente"]
                        boleta_aux.save()
                    Notificacion.objects.create(usuario=usuario,
                                                titulo='Reserva de Boletas para ' + str(pelicula.nombre),
                                                mensaje='Se ha confirmado la reserva de ' + str(
                                                    len(sillas)) + ' boletas por un valor de $' + str(
                                                    precio_final), tipo=3)
                    messages.success(request, 'Boletas Reservadas exitosamente!')
                    return redirect('accounts:home')
                else:
                    messages.error(request, 'El usuario no tiene saldo suficiente')
                    return redirect('accounts:consultar_saldo')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'boletas/reservar_boleta.html',
                          {'form': form, 'itemlist': list(range(0, 26)),
                           'sillas': consultar_sala_comprar(id_funcion),
                           'pelicula': pelicula, 'funcion': funcion, 'tipo_sala': tipo_sala})
    else:
        form = CrearBoletaForm()
        form.fields['funcion'].initial = funcion
        form.fields['medio_pago'].initial = 'saldo'
        form.fields['cedula'].initial = usuario.cedula
        form.fields['nombre_cliente'].initial = usuario.get_full_name()

        return render(request, 'boletas/reservar_boleta.html', {'form': form, 'itemlist': list(range(0, 26)),
                                                               'sillas': consultar_sala_comprar(id_funcion),
                                                               'pelicula': pelicula, 'funcion': funcion,
                                                               'tipo_sala': tipo_sala})


def pagar_reserva(request):
    usuario = request.user
    if request.method == 'POST':
        boletas_pagadas = request.POST.getlist('boletas_reservadas')
        boletas = Boleta.objects.filter(id__in=boletas_pagadas)
        boletas.update(reserva=False)
        boletas_ids =boletas.values_list('id', flat=True)
        messages.success(request, 'Reservas Pagadas exitosamente!')
        return render(request, 'boletas/pdf_boleta.html', {'boletas_ids': boletas_ids})

    if request.method == 'GET':
        form = PagarReservaForm()
        return render(request, 'boletas/pagar_reserva.html', {'form': form})


def get_boletas_reservadas(request):
    if request.is_ajax():
        id_cliente = request.GET.get('id_cliente', None)
        try:
            cliente = User.objects.get(cedula=str(id_cliente))
            boletas_reservadas = Boleta.objects.filter(cedula=cliente.cedula, reserva=True)
            boletas_json = []
            for boleta in boletas_reservadas:
                boleta_json = {'id': boleta.id, 'text': boleta.funcion.pelicula.nombre + " | " + boleta.silla.nombre}
                boletas_json.append(boleta_json)
            return JsonResponse({'boletas_reservadas': boletas_json})

        except Funcion.DoesNotExist:
            return JsonResponse({'response': 0})


def vender_boleta(request):
    usuario = request.user
    empleado = Empleado.objects.get(user=usuario)
    peliculas = Pelicula.objects.filter(funcion__sala__sucursal_id=empleado.sucursal.id)
    # peliculas = Pelicula.get_pelicula_estreno(True)

    if request.method == 'POST':
        lista_sillas = request.POST.get('boletas', None)
        id_funcion = request.POST.get('funcion', None)
        precio_final = request.POST.get('precio_final', None)
        medio_pago = request.POST.get('pago_cliente', None)
        funcion = Funcion.objects.get(id=id_funcion)
        pelicula = Pelicula.objects.get(funcion=funcion)
        tipo_sala = funcion.sala.tipo_sala
        sillas = eval(lista_sillas)
        boletas_ids = []
        flag_error = False
        for silla in sillas:
            i = silla['i']
            j = silla['j']
            tipo = silla['color']
            silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
            boleta_funcion = Boleta.objects.filter(funcion=funcion, silla=silla_aux)
            if boleta_funcion.count() != 0:
                flag_error = True

        if flag_error:
            messages.error(request, 'Hay algunas sillas que no están disponibles')

        form = CrearBoletaForm(request.POST)
        if form.is_valid() and not flag_error:
            if medio_pago == 'saldo':
                try:
                    usuario = User.objects.get(cedula=form.data["cedula"])
                    saldo_actual = usuario.cliente.saldo
                    if saldo_actual >= int(precio_final):
                        for silla in sillas:
                            i = silla['i']
                            j = silla['j']
                            tipo = silla['color']
                            silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)

                            # Calculo del precio boleta
                            tipo_silla = silla_aux.tipo

                            precio_silla = {
                                'GENERAL': 2000,
                                'PREFERENCIAL': 3000,
                                'DISCAPACITADO': 1000
                            }

                            precio_sala = {
                                "SALA_GENERAL": 4000,
                                "SALA_IMAX":  5000,
                                "SALA_3D":  4500,
                                "SALA_4DX": 6000
                            }
                            boleta_aux = Boleta()
                            boleta_aux.total = precio_silla[tipo_silla] + precio_sala[funcion.sala.tipo_sala]
                            boleta_aux.funcion = funcion
                            boleta_aux.silla = silla_aux
                            boleta_aux.medio_pago = form.cleaned_data['medio_pago']
                            boleta_aux.cedula = form.data["cedula"]
                            boleta_aux.cedula_empleado = usuario.cedula
                            boleta_aux.nombre_cliente = form.data["nombre_cliente"]
                            boleta_aux.save()
                            boletas_ids.append(boleta_aux.id)
                        usuario.cliente.saldo = saldo_actual - int(precio_final)
                        usuario.cliente.save()
                        Notificacion.objects.create(usuario=usuario,
                                                    titulo='Compra de Boletas para ' + str(pelicula.nombre),
                                                    mensaje='Se ha confirmado la compra de ' + str(
                                                len(sillas)) + ' boletas por un valor de $' + str(
                                                        precio_final), tipo=3)
                        messages.success(request, 'Boletas vendidas exitosamente!')
                        return render(request, 'boletas/pdf_boleta.html', {'boletas_ids': boletas_ids})
                    else:
                        messages.error(request, 'El usuario no tiene saldo suficiente')
                        return render(request, 'boletas/vender_boleta.html',
                                      {'form': form, 'itemlist': list(range(0, 26)), 'lista_sillas': 'lista_sillas',
                                       'peliculas': peliculas,
                                       'form_saldo': SaldoForm()})

                except(User.cliente.RelatedObjectDoesNotExist, User.DoesNotExist):
                    messages.error(request, 'El usuario no puede pagar con saldo')
                    return render(request, 'boletas/vender_boleta.html',
                                  {'form': form, 'itemlist': list(range(0, 26)), 'lista_sillas': 'lista_sillas',
                                   'peliculas': peliculas,
                                   'form_saldo': SaldoForm()})

            elif medio_pago == 'efectivo':
                for silla in sillas:
                    i = silla['i']
                    j = silla['j']
                    tipo = silla['color']
                    silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
                    boleta_aux = Boleta()

                    # Calculo del precio boleta
                    tipo_silla = silla_aux.tipo

                    precio_silla = {
                        'GENERAL': 2000,
                        'PREFERENCIAL': 3000,
                        'DISCAPACITADO': 1000
                    }

                    precio_sala = {
                        "SALA_GENERAL": 4000,
                        "SALA_IMAX": 5000,
                        "SALA_3D": 4500,
                        "SALA_4DX": 6000
                    }
                    boleta_aux.total = precio_silla[tipo_silla] + precio_sala[funcion.sala.tipo_sala]
                    boleta_aux.funcion = funcion
                    boleta_aux.silla = silla_aux
                    boleta_aux.medio_pago = form.cleaned_data['medio_pago']
                    boleta_aux.cedula = form.data["cedula"]
                    boleta_aux.cedula_empleado = usuario.cedula
                    boleta_aux.nombre_cliente = form.data["nombre_cliente"]
                    boleta_aux.save()
                    boletas_ids.append(boleta_aux.id)
                messages.success(request, 'Boletas vendidas exitósamente!')
                return render(request, 'boletas/pdf_boleta.html',{'boletas_ids': boletas_ids})

        else:
            boletas_compradas = Boleta.objects.filter(funcion=funcion)
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'boletas/vender_boleta.html',
                          {'form': form, 'itemlist': list(range(0, 26)), 'lista_sillas': 'lista_sillas',
                           'peliculas': peliculas,
                           'form_saldo': SaldoForm()})
    else:
        form = CrearBoletaForm()
        return render(request, 'boletas/vender_boleta.html', {'form': form, 'itemlist': list(range(0, 26)),
                                                              'lista_sillas': 'lista_sillas', 'peliculas': peliculas,
                                                              'form_saldo': SaldoForm()})


def comprar_boleta(request,slug, id_funcion):
    usuario = request.user
    funcion = Funcion.objects.get(id=id_funcion)
    pelicula = Pelicula.objects.get(funcion=funcion)
    tipo_sala = funcion.sala.tipo_sala

    if request.method == 'POST':
        lista_sillas = request.POST.get('boletas', None)
        precio_final = request.POST.get('precio_final', None)
        funcion = Funcion.objects.get(id=id_funcion)
        sillas = eval(lista_sillas)
        flag_error = False
        for silla in sillas:
            i = silla['i']
            j = silla['j']
            tipo = silla['color']
            silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
            boleta_funcion = Boleta.objects.filter(funcion=funcion, silla=silla_aux)
            if boleta_funcion.count() != 0:
                flag_error = True

        if flag_error:
            messages.error(request, 'Hay algunas sillas que no están disponibles')

        form = CrearBoletaForm(request.POST)
        if form.is_valid() and not flag_error:
            if form.cleaned_data['medio_pago'] == 'saldo':
                try:
                    usuario = User.objects.get(cedula=form.data["cedula"])
                    saldo_actual = usuario.cliente.saldo
                    if saldo_actual >= int(precio_final):
                        for silla in sillas:
                            i = silla['i']
                            j = silla['j']
                            tipo = silla['color']
                            silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
                            boleta_aux = Boleta()
                            # Calculo del precio boleta
                            tipo_silla = silla_aux.tipo

                            precio_silla = {
                                'GENERAL': 2000,
                                'PREFERENCIAL': 3000,
                                'DISCAPACITADO': 1000
                            }

                            precio_sala = {
                                "SALA_GENERAL": 4000,
                                "SALA_IMAX": 5000,
                                "SALA_3D": 4500,
                                "SALA_4DX": 6000
                            }
                            boleta_aux.total = precio_silla[tipo_silla] + precio_sala[funcion.sala.tipo_sala]
                            boleta_aux.funcion = funcion
                            boleta_aux.medio_pago = form.cleaned_data['medio_pago']
                            boleta_aux.silla = silla_aux
                            boleta_aux.cedula = form.data["cedula"]
                            boleta_aux.cedula_empleado = usuario.cedula
                            boleta_aux.nombre_cliente = form.data["nombre_cliente"]
                            boleta_aux.save()
                        usuario.cliente.saldo = saldo_actual - int(precio_final)
                        usuario.cliente.save()
                        messages.success(request, 'Boletas compradas exitosamente!')
                        Notificacion.objects.create(usuario=usuario, titulo='Compra de Boletas para '+str(pelicula.nombre),
                                                    mensaje='Se ha confirmado la compra de ' + str(
                                                len(sillas)) + ' boletas por un valor de $'+str(precio_final),
                                                    tipo=3)
                        return redirect('accounts:home')
                    else:
                        messages.error(request, 'No tienes saldo suficiente')
                        return render(request, 'boletas/comprar_boleta.html',
                                      {'form': form, 'itemlist': list(range(0, 26)),
                                       'sillas': consultar_sala_comprar(id_funcion),
                                       'pelicula': pelicula, 'funcion': funcion, 'tipo_sala': tipo_sala})

                except(User.cliente.RelatedObjectDoesNotExist, User.DoesNotExist):
                    messages.error(request, 'El usuario no puede pagar con saldo')
                    return render(request, 'boletas/comprar_boleta.html',
                                  {'form': form, 'itemlist': list(range(0, 26)),
                                   'sillas': consultar_sala_comprar(id_funcion),
                                   'pelicula': pelicula, 'funcion': funcion, 'tipo_sala': tipo_sala})

            elif form.cleaned_data['medio_pago'] == 'efectivo':
                for silla in sillas:
                    i = silla['i']
                    j = silla['j']
                    tipo = silla['color']
                    silla_aux = Silla.objects.get(ubicacion_x=i, ubicacion_y=j, sala=funcion.sala)
                    boleta_aux = Boleta()
                    # Calculo del precio boleta
                    tipo_silla = silla_aux.tipo

                    precio_silla = {
                        'GENERAL': 2000,
                        'PREFERENCIAL': 3000,
                        'DISCAPACITADO': 1000
                    }

                    precio_sala = {
                        "SALA_GENERAL": 4000,
                        "SALA_IMAX": 5000,
                        "SALA_3D": 4500,
                        "SALA_4DX": 6000
                    }
                    boleta_aux.total = precio_silla[tipo_silla] + precio_sala[funcion.sala.tipo_sala]
                    boleta_aux.funcion = funcion
                    boleta_aux.silla = silla_aux
                    boleta_aux.medio_pago = form.cleaned_data['medio_pago']
                    boleta_aux.cedula = form.data["cedula"]
                    boleta_aux.cedula_empleado = usuario.cedula
                    boleta_aux.nombre_cliente = form.data["nombre_cliente"]
                    boleta_aux.save()
                messages.success(request, 'Boletas compradas exitosamente!')
                return redirect('accounts:home')
        else:
            boletas_compradas = Boleta.objects.filter(funcion=funcion)
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'boletas/comprar_boleta.html',
                          {'form': form, 'itemlist': list(range(0, 26)),
                           'sillas': consultar_sala_comprar(id_funcion),
                           'pelicula': pelicula, 'funcion': funcion, 'tipo_sala': tipo_sala})
    else:
        form = CrearBoletaForm()
        form.fields['funcion'].initial = funcion
        if not usuario.is_anonymous:
            form.fields['cedula'].initial = usuario.cedula
            form.fields['nombre_cliente'].initial = usuario.get_full_name()
            form.fields['medio_pago'].initial = 'saldo'

        return render(request, 'boletas/comprar_boleta.html', {'form': form, 'itemlist': list(range(0, 26)),
                                                               'sillas': consultar_sala_comprar(id_funcion),
                                                               'pelicula': pelicula, 'funcion': funcion,
                                                               'tipo_sala': tipo_sala})


def consultar_sala_comprar(funcion_id):
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
                pos = (i * 26) + j + 1
                silla = lista_sillas[pos]
                if silla:
                    if Boleta.objects.filter(funcion=funcion, silla=silla).exists():
                                html += '<div> <input id="' + str(i) + '-' + str(
                                j) + '" class="OCUPADO" onclick="myFunction(this)" type="checkbox" name="silla" value="{"i":"' + str(
                                i) + ',"j":' + str(j) + ',"color": "SIN_MARCAR"}" disabled=""> </div>'
                    else:
                        html += "<div> <input id='" + str(i) + "-" + str(
                        j) + "' class='" + silla.tipo + "' onclick='myFunction(this)' type='checkbox'  name='silla' hola='" + silla.nombre + "' checked value=" + "{'i':" + str(
                        i) + ",'j':" + str(j) + ",'color':'" + silla.tipo + "'}> </div>"

                else:
                    html += '<div> <input id="' + str(i) + '-' + str(
                        j) + '" class="SIN_MARCAR" onclick="myFunction(this)" type="checkbox" name="silla" value="{"i":"' + str(
                        i) + ',"j":' + str(j) + ',"color": "SIN_MARCAR"}" disabled=""> </div>'
            html += '</div>'
        return html

    except Funcion.DoesNotExist:
        return 0


def consultar_pelicula(request):
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            return JsonResponse({'sinopsis': pelicula.sinopsis})
        except Pelicula.DoesNotExist:
            return JsonResponse({'response': 0})


def consultar_funciones(request):
    usuario = request.user
    if request.is_ajax():
        pelicula_id = request.GET.get('pelicula_id', None)
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            empleado = Empleado.objects.get(user=usuario)
            funciones = Funcion.objects.filter(sala__sucursal=empleado.sucursal, pelicula=pelicula)
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
                    pos = (i * 26) + j + 1
                    silla = lista_sillas[pos]
                    if silla:
                        html += "<div> <input id='" + str(i) + "-" + str(
                            j) + "' class='" + silla.tipo + "' onclick='myFunction(this)' type='checkbox'  name='silla' hola='" + silla.nombre + "' checked value=" + "{'i':" + str(
                            i) + ",'j':" + str(j) + ",'color':'" + silla.tipo + "'}> </div>"
                    else:
                        html += '<div> <input id="' + str(i) + '-' + str(
                            j) + '" class="SIN_MARCAR" onclick="myFunction(this)" type="checkbox" name="silla" value="{"i":"' + str(
                            i) + ',"j":' + str(j) + ',"color": "SIN_MARCAR"}" disabled=""> </div>'

                html += '</div>'
            return JsonResponse({'html': html, 'tipo_sala': sala.tipo_sala})

        except Funcion.DoesNotExist:
            return JsonResponse({'response': 0})


def consultar_boletas_ocupadas(id_funcion):
    try:
        funcion = Funcion.objects.get(id=id_funcion)
        boletas_fumcion = Boleta.objects.filter(funcion=funcion)
        boletas_json = []
        for boleta in boletas_fumcion:
            boleta_json = {"i": boleta.silla.ubicacion_x, "j": boleta.silla.ubicacion_y}
            boletas_json.append(boleta_json)
        return JsonResponse({'boletas_funcion': boletas_json})

    except Funcion.DoesNotExist:
        return JsonResponse({'response': 0})


def consultar_boletas_funcion(request):
    if request.is_ajax():
        funcion_id = request.GET.get('funcion_id', None)
        try:
            funcion = Funcion.objects.get(id=int(funcion_id))
            boletas_fumcion = Boleta.objects.filter(funcion=funcion)
            boletas_json = []
            for boleta in boletas_fumcion:
                boleta_json = {"i": boleta.silla.ubicacion_x, "j": boleta.silla.ubicacion_y}
                boletas_json.append(boleta_json)
            return JsonResponse({'boletas_funcion': boletas_json})

        except Funcion.DoesNotExist:
            return JsonResponse({'response': 0})
