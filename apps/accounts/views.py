from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import *
from django.contrib import messages
from apps.peliculas.models import *
from apps.peliculas.models import Pelicula
from apps.sucursales.models import *


def checkusername(request):
    if request.is_ajax():
        username = request.GET.get('username', None)
    if username:
        u = User.objects.filter(username=username).count()
        if u==0: response = True #Si el username esta disponible es True
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


@login_required
def home(request):
    usuario = request.user
    if usuario.is_staff:
        return render(request, 'accounts/home_admin.html', {'user': usuario, 'datos': datos_dashboard()})
    elif usuario.is_cliente:
        return render(request, 'accounts/home_cliente.html', {'user': usuario, 'sucursales': Sucursal.get_info(),
                                                              'peliculas1': Pelicula.get_peliculas().filter(is_estreno=True), 'peliculas2': Pelicula.get_peliculas().filter(is_estreno=False)})
    elif usuario.get_cargo_empleado() == 'Gerente':
        return render(request, 'accounts/home_gerente.html', {'user': usuario, 'datos': datos_dashboard_gerente()})
    elif usuario.get_cargo_empleado() == 'Operador':
        return render(request, 'accounts/home_operador.html', {'user': usuario, 'datos':
            datos_dashboard_operador(), 'peliculas': Pelicula.get_peliculas().filter(is_estreno=True)})


def signup(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if True:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            user_data = FormEmpleado(request.POST)
            if form.is_valid() and user_data.is_valid():
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


def signup_cliente(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_data = FormCliente(request.POST)
        if form.is_valid() and user_data.is_valid():

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
    empleado = Empleado.objects.get(id = id_user)
    user = User.objects.get(empleado = empleado)
    usuario = request.user

    if True:
        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=user)
            form_empleado = FormEmpleado(request.POST, instance=empleado)
            if form.is_valid() and form_empleado.is_valid():
                form.save()
                form_empleado.save()
                messages.success(request, 'Has modificado el empleado exitosamente!')
                return redirect('accounts:registro')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/editar_empleado.html', {'form': form, 'form_empleado': form_empleado})

        else:
            form = EditUserForm(instance=user)
            form_empleado = FormEmpleado(instance=empleado)
            return render(request, 'accounts/editar_empleado.html', {'form': form, 'form_empleado': form_empleado})

    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def editar_perfil(request):

    usuario = request.user
    if usuario.is_cliente or usuario.is_staff:
        cliente = Cliente.objects.get(user = usuario)
        if request.method == 'POST':
            form = EditarUsuario(request.POST, instance=usuario)
            form_cliente = FormCliente(request.POST, instance=cliente)
            if form.is_valid() and form_cliente.is_valid():
                form.save()
                form_cliente.save()
                messages.success(request, 'Has modificado tu perfil exitosamente!')
                return redirect('accounts:home')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/editar_perfil_cliente.html',
                              {'form': form, 'form_cliente': form_cliente})

        else:
            form = EditarUsuario(instance=usuario)
            form_cliente = FormCliente(instance=cliente)
            return render(request, 'accounts/editar_perfil_cliente.html', {'form': form, 'form_cliente': form_cliente})
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
    num_peliculas_estreno = Pelicula.objects.filter(is_estreno=True).count()
    num_salas = 0
    datos = {
        'num_peliculas_estreno': num_peliculas_estreno,
        'num_salas': num_salas
    }

    return datos


def datos_dashboard_operador():
    num_peliculas_estreno = Pelicula.objects.filter(is_estreno=True).count()
    datos = {
        'num_peliculas_estreno': num_peliculas_estreno,
    }

    return datos
