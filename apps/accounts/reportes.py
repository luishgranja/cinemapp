import datetime
from django.db.models import Max, Count
from apps.sucursales.models import *
from apps.boletas.models import *
from apps.accounts.models import *
from apps.peliculas.models import *


# Reporte ventas diarias por año y mes

def reporte_ventas_diarias(y, m):
    data = []
    sucursales = Sucursal.objects.all()
    for i in range(1, 31):
        datos_dia = {'y': 'Día  ' + str(i)}
        for sucursal in sucursales:
            boletas = Boleta.objects.filter(funcion__sala__sucursal=sucursal, fecha_compra__month=m,
                                            fecha_compra__day=i, fecha_compra__year=y)
            valor_total = 0
            for boleta in boletas:
                valor_total += boleta.total
            datos_dia.update({str(sucursal.nombre): str(valor_total)})
        data.append(datos_dia)
    return data


# Reporte venta boletas diarias por año y mes

def reporte_boletas_diarias(y, m):
    data = []
    sucursales = Sucursal.objects.all()
    for i in range(1, 31):
        datos = {'y': 'Día  ' + str(i)}
        for sucursal in sucursales:
            boletas = Boleta.objects.filter(funcion__sala__sucursal=sucursal, fecha_compra__month=m,
                                            fecha_compra__day=i, fecha_compra__year=y)
            total = boletas.count()
            datos.update({str(sucursal.nombre): str(total)})
        data.append(datos)
    return data


# Reporte numero de boletas compradas clientes registrados vs anonimos
def reporte_clientes(y, m):
    datos = []
    boletas = Boleta.objects.filter(fecha_compra__month=m, fecha_compra__year=y).values('cedula')

    num_clientes_registrados = Boleta.objects.filter(cedula__in=boletas, cedula_empleado__in=boletas).count()
    num_no_registrados = Boleta.objects.filter(fecha_compra__month=m, fecha_compra__year=y).count() - num_clientes_registrados

    datos.append({'label': "Registrados", 'value': str(num_clientes_registrados)})
    datos.append({'label': "No registrados", 'value': str(num_no_registrados)})

    return datos


# Reporte numero de boletas compradas por pelicula
def reporte_peliculas(y, m, n):
    datos = []
    peliculas = Pelicula.objects.filter(funcion__boleta__fecha_compra__month=m, funcion__fecha_funcion__year=y).values('id').annotate(contador=Count('id')).order_by('-contador')

    if n > peliculas.count():
        return datos

    for i in range(0, n):
        pelicula = Pelicula.objects.get(id=peliculas[i]['id'])
        datos.append({'label': str(pelicula.nombre), 'value': str(peliculas[i]['contador'])})

    return datos


