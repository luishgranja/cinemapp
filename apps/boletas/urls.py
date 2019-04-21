from django.urls import path
from apps.boletas.views import *

app_name = 'boletas'

urlpatterns = [
    path('vender-boleta', vender_boleta, name='vender_boleta'),
    path('ver-boletas', ver_boletas, name='ver_boletas'),
    path('generar-boleta/<int:id_boleta>', generar_boleta, name='generar_boleta'),
    path('comprar-boleta/<slug:slug>/<int:id_funcion>', comprar_boleta, name='comprar_boleta'),
    path('reservar-boleta/<slug:slug>/<int:id_funcion>', crear_reserva, name='crear_reserva'),
    path('pagar-reserva', pagar_reserva, name='pagar_reserva'),
    path('api/consultar-pelicula', consultar_pelicula, name='consultar_pelicula'),
    path('api/consultar_boletas_reservadas', get_boletas_reservadas, name='get_boletas_reservadas'),
    path('api/consultar-funciones', consultar_funciones, name='consultar_funciones'),
    path('api/consultar-sala', consultar_sala, name='consultar_sala'),
    path('api/consultar-boletas-funcion', consultar_boletas_funcion, name='consultar_boletas_funcion'),
    path('api/cancelar_boleta', cancelar_boleta, name='cancelar_boleta'),

]
