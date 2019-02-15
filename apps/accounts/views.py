#Commit de prueba

from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.forms import *
from apps.accounts.models import *
from apps.peliculas.models import *
from apps.sucursales.models import *
from apps.peliculas.views import *
from apps.accounts.decorators import check_recaptcha


# Funcion para cambiar el estado de una notificacion a leida

def notificacion_leida(request):
    if request.is_ajax():
        id_notificacion = request.GET.get('id', None)
        if id_notificacion:
            notificacion = Notificacion.objects.filter(id=id_notificacion).update(leido=True)
        return JsonResponse({'response':'ok'})


# Funcion para verificar que un username esta disponible
# Devuelve true si esta disponible, false si NO esta disponible

def checkusername(request):
    if request.is_ajax():
        username = request.GET.get('username', None)
    if username:
        u = User.objects.filter(username=username).count()
        # Si el username esta disponible es True
        if u == 0: response = True
        else: response = False
    return JsonResponse({'response': response})


def get_sucursales_disponibles(request):
    if request.is_ajax():
        id_cargo = request.GET.get('id_cargo', None)

    sucursales = Sucursal.objects.all()
    gerentes = Empleado.objects.filter(cargo='Gerente')
    sucursales_no_gerente = []
    sucursales_total = []

    for sucursal in sucursales:
        id_sucursal = sucursal.id
        flag = 0
        sucursales_total.append({'id': sucursal.id, 'text': sucursal.nombre})
        for gerente in gerentes:
            if gerente.sucursal is not None and gerente.sucursal.id == id_sucursal:
                flag += 1
        if flag == 0:
            sucursales_no_gerente.append({'id': sucursal.id, 'text': sucursal.nombre})

    sucursales_no_gerente_response = {'sucursales': sucursales_no_gerente}
    sucursal_total_response ={'sucursales': sucursales_total}

    if id_cargo == 'Gerente':
        return JsonResponse(sucursales_no_gerente_response)
    elif id_cargo == 'Operador':
        return JsonResponse(sucursal_total_response)


# Consulta todas las notificaciones que el usuario NO ha leido
def notificaciones(user):
    notis_all = Notificacion.objects.filter(usuario=user)
    notis = notis_all & Notificacion.objects.filter(leido=False)
    num_notis = notis.filter(leido=False).count()

    notificaciones = {
        'num_notis': num_notis,
        'notis': notis
    }
    return notificaciones

# Consulta todas las notificaciones del usuario
def notis_all(user):
    notis = Notificacion.objects.filter(usuario=user)
    notificaciones = {
        'notis_all': notis
    }
    return notificaciones

def consultar_notificaciones(request):
    usuario = request.user
    if request.method == 'GET':
        return render(request, 'accounts/notificaciones.html',
        {'notis_all':notis_all(usuario), 'notis':notificaciones(usuario), 'sucursales': Sucursal.get_info()})

@login_required
def home(request):
    usuario = request.user
    if usuario.is_staff:
        return render(request, 'accounts/home_admin.html', {'notis':notificaciones(usuario),'user': usuario, 'datos': datos_dashboard()})
    elif usuario.is_cliente:
        return render(request, 'accounts/home_cliente.html', {'notis':notificaciones(usuario),'user': usuario, 'sucursales': Sucursal.get_info(),
                                                              'peliculas1': listar_cartelera(), 'peliculas2': listar_peliculas_proximo_estreno()})
    elif usuario.get_cargo_empleado() == 'Gerente':
        return render(request, 'accounts/home_gerente.html', {'user': usuario, 'datos': datos_dashboard_gerente()})
    elif usuario.get_cargo_empleado() == 'Operador':
        return render(request, 'accounts/home_operador.html', {'user': usuario, 'datos':
            datos_dashboard_operador(), 'peliculas': listar_cartelera(), 'form_saldo': CargarSaldoForm()})

def signup(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if usuario.is_staff:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            user_data = FormEmpleado(request.POST)
            if form.is_valid() and user_data.is_valid() and request.recaptcha_is_valid:
                messages.success(request, 'Empleado registrado exitosamente')

                user = form.save(commit=False)
                user.save()
                user_extra = user_data.save(commit=False)
                user_extra.user = user
                user_extra.save()

                return render(request, 'accounts/signup.html',
                              {'form': SignUpForm(), 'form_empleado': FormEmpleado(), 'empleados': listar_empleados()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/signup.html', {'form': form, 'form_empleado': user_data})
        else:
            form = SignUpForm()
            form_empleado = FormEmpleado()
            return render(request, 'accounts/signup.html',
                          {'form': form, 'form_empleado': form_empleado, 'empleados': listar_empleados()})
    # En caso de que el usuario no sea admin se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


@check_recaptcha
def signup_cliente(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_data = FormCliente(request.POST)
        if form.is_valid() and user_data.is_valid() and request.recaptcha_is_valid:

            user = form.save(commit=False)
            user.is_cliente = True
            user.save()

            user_extra = user_data.save(commit=False)
            user_extra.user = user
            user_extra.save()
            if request.user.is_anonymous:
                login(request, user)

            return redirect('accounts:login')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'accounts/signup_cliente.html', {'form': form, 'user_form': user_data})
    else:
        form = SignUpForm()
        user_data = FormCliente()
        return render(request, 'accounts/signup_cliente.html', {'form': form, 'user_form': user_data})


def listar_empleados():
    return Empleado.get_info()


def editar_empleado(request, id_user):
    empleado = Empleado.objects.get(id=id_user)
    user = User.objects.get(empleado=empleado)
    usuario = request.user

    if usuario.is_staff:
        if request.method == 'POST':
            form = EditarEmpleado(request.POST, instance=user)
            form_empleado = FormEmpleado(request.POST, instance=empleado)
            form_empleado_extra = EditarEmpleadoExtra(request.POST, instance=user)
            if form.is_valid() and form_empleado.is_valid() and form_empleado_extra.is_valid():
                form.save()
                form_empleado.save()
                form_empleado_extra.save()
                messages.success(request, 'Has modificado el empleado exitosamente!')
                return redirect('accounts:registro')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/editar_empleado.html', {'form': form, 'form_empleado': form_empleado, 'form_empleado_extra': form_empleado_extra})

        else:
            form = EditarEmpleado(instance=user)
            form_empleado = FormEmpleado(instance=empleado)
            form_empleado_extra = EditarEmpleadoExtra(instance=user)
            return render(request, 'accounts/editar_empleado.html', {'form': form, 'form_empleado': form_empleado, 'form_empleado_extra': form_empleado_extra})

    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')

def editar_perfil_empleado(request):
    usuario = request.user
    if not (request.user.is_anonymous or usuario.is_cliente):
        mi_empleado = User.objects.get(id=usuario.id)
        if request.method == 'POST':
            form = EditarEmpleado(request.POST, instance=mi_empleado)
            if form.is_valid():
                form.save()
                messages.success(request, 'Has modificado tu perfil exitosamente!')
                return redirect('accounts:home')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/editar_perfil_empleado.html',
                              {'form': form})

        else:
            form = EditarEmpleado(instance=mi_empleado)
            return render(request, 'accounts/editar_perfil_empleado.html', {'form': form})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def editar_perfil(request):
    usuario = request.user
    if not request.user.is_anonymous and usuario.is_cliente:
        cliente = Cliente.objects.get(user=usuario)
        if request.method == 'POST':
            form = EditarPerfilCliente(request.POST, instance=usuario)
            form_cliente = FormCliente(request.POST, instance=cliente)
            if form.is_valid() and form_cliente.is_valid():
                form.save()
                form_cliente.save()
                messages.success(request, 'Has modificado tu perfil exitosamente!')
                return redirect('accounts:home')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/editar_perfil_cliente.html',
                              {'form': form, 'form_cliente': form_cliente, 'sucursales': Sucursal.get_info()})

        else:
            form = EditarPerfilCliente(instance=usuario)
            form_cliente = FormCliente(instance=cliente)
            return render(request, 'accounts/editar_perfil_cliente.html', {'form': form, 'form_cliente': form_cliente, 'sucursales': Sucursal.get_info()})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def datos_dashboard():
    num_empleados = Empleado.objects.all().count()
    num_peliculas_estreno = Pelicula.objects.filter(is_estreno=True).count()
    num_sucursales = Sucursal.objects.all().count()
    num_clientes = Cliente.objects.all().count()

    sucursales = Sucursal.objects.all()
    gerentes = Empleado.objects.filter(cargo='Gerente')
    sucursales_no_gerente = []

    for sucursal in sucursales:
        id_sucursal = sucursal.id
        flag = 0
        for gerente in gerentes:
            if gerente.sucursal is not None and gerente.sucursal.id == id_sucursal:
                flag += 1
        if flag == 0:
            sucursales_no_gerente.append({'nombre': sucursal.nombre, 'id': sucursal.id})

    datos = {
        'num_empleados': num_empleados,
        'num_peliculas_estreno': num_peliculas_estreno,
        'num_sucursales': num_sucursales,
        'num_clientes': num_clientes,
        'sucursales_no_gerente': sucursales_no_gerente
    }

    return datos


def datos_dashboard_gerente():
    num_peliculas_cartelera = (Pelicula.get_pelicula_estreno(True) & Pelicula.get_peliculas_activas()).count()
    num_proximos_estrenos = (Pelicula.get_pelicula_estreno(False) & Pelicula.get_peliculas_activas()).count()
    num_salas = 0
    datos = {
        'num_peliculas_cartelera': num_peliculas_cartelera,
        'num_proximos_estrenos': num_proximos_estrenos,
        'num_salas': num_salas
    }

    return datos


def datos_dashboard_operador():
    num_proximos_estrenos = (Pelicula.get_pelicula_estreno(False) & Pelicula.get_peliculas_activas()).count()
    datos = {
        'num_proximos_estrenos': num_proximos_estrenos,
    }
    return datos


def consultar_cliente(request):

    if request.is_ajax():
        cedula = request.GET.get('cedula', None)
        try:
            cliente = User.objects.get(cedula=cedula)
            nombre = cliente.get_full_name()
            saldo = cliente.cliente.saldo
            return JsonResponse({'saldo': saldo, 'nombre': nombre})
        except (User.cliente.RelatedObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'saldo': '--------', 'nombre': 'No existe un cliente con la cédula ingresada'})


def cargar_saldo(request):
    if request.is_ajax():
        cedula = request.GET.get('cedula', None)
        saldo = request.GET.get('saldo', 0)
        try:
            cliente = User.objects.get(cedula=cedula)
            saldo_actual = cliente.cliente.saldo

            cliente.cliente.saldo = int(saldo) + saldo_actual
            cliente.cliente.save()
            return JsonResponse({'saldo': 0})

        except (User.cliente.RelatedObjectDoesNotExist, User.DoesNotExist):
            return JsonResponse({'saldo': 0})

    return JsonResponse({'error':'error'})