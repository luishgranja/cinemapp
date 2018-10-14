from django.urls import path , include
from apps.accounts.views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [

    path('registro/empleados', signup, name='registro'),
    path('registro/', signup_cliente, name='registro_cliente'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', home, name='home'),

]