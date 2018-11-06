from django.urls import path , include
from apps.accounts.views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('gestion-empleados', signup, name='registro'),
    path('registrarse', signup_cliente, name='registro_cliente'),
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard', home, name='home'),
    path('editar/empleado/<int:id_user>', editar_empleado, name='modificar_empleado'),
    path('editar-perfil-empleado', editar_perfil, name='editar_perfil_empleado'),
    path('editar-perfil', editar_perfil, name='editar_perfil_cliente'),
    path('consulta_sucursales', get_sucursales_disponibles, name= 'get_sucursales_disponibles'),
    path('consulta_username', checkusername, name='checkusername'),

]
