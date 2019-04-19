from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from apps.accounts.decorators import check_recaptcha
from apps.funciones.models import *
from datetime import date, timedelta


@check_recaptcha
def crear_pelicula(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if usuario.is_staff or True:
        if request.method == 'POST':
            form = CrearPeliculaForm(request.POST, request.FILES)
            if form.is_valid() and request.recaptcha_is_valid:
                form.save()
                messages.success(request, 'Película registrada exitosamente')
                return render(request, 'peliculas/crear_peliculas.html', {'form': CrearPeliculaForm(), 'peliculas': listar_peliculas()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'peliculas/crear_peliculas.html', {'form': form, 'peliculas': listar_peliculas()})
        else:
            form = CrearPeliculaForm()
            return render(request, 'peliculas/crear_peliculas.html', {'form': form, 'peliculas': listar_peliculas()})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def listar_peliculas():
    return Pelicula.get_peliculas()


def listar_cartelera():
    fecha_actual = date.today()
    funciones = Funcion.objects.filter(fecha_funcion__range=(fecha_actual, fecha_actual + timedelta(days=15)))
    peliculas = Pelicula.objects.filter(funcion__in=funciones)
    return (Pelicula.get_pelicula_estreno(True) & Pelicula.get_peliculas_activas() & peliculas).distinct()


def listar_cartelera_sucursal(sucursal):
    peliculas = Pelicula.objects.filter(funcion__sala__sucursal_id=sucursal).distinct()
    return peliculas


def listar_peliculas_proximo_estreno():
    return Pelicula.get_pelicula_estreno(False) & Pelicula.get_peliculas_activas()


@check_recaptcha
def editar_pelicula(request, id_pelicula):
    usuario = request.user
    pelicula = Pelicula.objects.get(id=id_pelicula)

    if True:
        if request.method == 'POST':
            form = CrearPeliculaForm(request.POST, request.FILES, instance=pelicula)
            if form.is_valid() and request.recaptcha_is_valid:
                form.save()
                messages.success(request, 'Película modificada exitosamente!')
                return redirect('peliculas:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'peliculas/editar_pelicula.html', {'form': form})
        else:
            form = CrearPeliculaForm(instance=pelicula)
            return render(request, 'peliculas/editar_pelicula.html', {'form': form})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def consultar_cartelera(request):
    return render(request,'peliculas/consultar_peliculas.html', {'peliculas': listar_cartelera()})


def consultar_proximos_estrenos(request):
    return render(request,'peliculas/consultar_peliculas.html', {'peliculas': listar_peliculas_proximo_estreno()})


def listar_pelicula(slug):
    return Pelicula.get_pelicula(slug)


def ver_pelicula(request, slug):
    usuario = request.user
    pelicula = listar_pelicula(slug)

    if usuario.is_staff or not usuario.is_cliente:
        base_template_name = 'base.html'

        try:
            empleado = Empleado.objects.get(user=usuario)
            funciones = Funcion.objects.filter(sala__sucursal=empleado.sucursal, pelicula=pelicula)
        except Empleado.DoesNotExist:
            funciones = Funcion.objects.filter(pelicula=pelicula)

    elif usuario.is_anonymous or usuario.is_cliente:
        base_template_name = 'base_cliente.html'
        funciones = Funcion.objects.filter(pelicula=pelicula)

    return render(request, 'peliculas/consultar_pelicula.html', {'peli': pelicula, 'funciones': funciones,
                                                                 'base_template_name': base_template_name})


def listar_generos():
    return Genero.get_generos()


@check_recaptcha
def crear_genero(request):
    usuario = request.user
    if request.method == 'POST':
        form = CrearGeneroForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            form.save()
            messages.success(request, 'Género creado exitósamente!')
            return render(request, 'peliculas/gestion_generos.html', {'form': CrearGeneroForm(), 'generos': listar_generos()})
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'peliculas/gestion_generos.html', {'form': form, 'generos': listar_generos()})
    else:
        form = CrearGeneroForm()
        return render(request, 'peliculas/gestion_generos.html', {'form': form, 'generos': listar_generos()})


def busqueda_peliculas(request):
    usuario = request.user
    if request.method == 'GET':
        nombre_pelicula = request.GET.get('q')
        peliculas = Pelicula.objects.filter(slug__icontains=nombre_pelicula)

        return render(request, 'peliculas/busqueda_peliculas.html', {'peliculas': peliculas,
                                                                     'nombre_pelicula': nombre_pelicula})


def get_template(usuario):
    if usuario.is_staff or not usuario.is_cliente:
        return 'base.html'
    elif usuario.is_anonymous or usuario.is_cliente:
        return 'base_cliente.html'
