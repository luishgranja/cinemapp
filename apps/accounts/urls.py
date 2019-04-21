from django.urls import path , include
from apps.accounts.views import *
from django.contrib.auth import views as auth_views
#from apps.accounts.decorators import check_recaptcha

app_name = 'accounts'

urlpatterns = [
    path('gestion-empleados', signup, name='registro'),
    path('registrarse', signup_cliente, name='registro_cliente'),
    path('', check_recaptcha(auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html')),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard', home, name='home'),
    path('ver-clientes', listar_clientes, name='clientes'),
    path('editar/empleado/<int:id_user>', editar_empleado, name='modificar_empleado'),
    path('editar-perfil-empleado', editar_perfil_empleado, name='editar_perfil_empleado'),
    path('editar-perfil', editar_perfil, name='editar_perfil_cliente'),
    path('api/consulta_sucursales', get_sucursales_disponibles, name= 'get_sucursales_disponibles'),
    path('api/consulta_username', checkusername, name='checkusername'),
    path('notificaciones', consultar_notificaciones, name='notificaciones'),
    path('api/notificacion_leida', notificacion_leida, name='notificacion_leida'),
    path('api/consultar_cliente', consultar_cliente, name='consultar_cliente'),
    path('api/cargar_saldo', cargar_saldo, name='cargar_saldo'),
    path('consultar-saldo', consultar_saldo, name='consultar_saldo'),
    path('guardar-saldo', guardar_saldo, name='guardar_saldo')

]
