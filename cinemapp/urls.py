
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('sucursales/', include('apps.sucursales.urls')),
    path('peliculas/', include('apps.peliculas.urls')),
    path('select2/', include('django_select2.urls')),
]
