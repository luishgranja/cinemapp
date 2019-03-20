from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('sucursales/', include('apps.sucursales.urls')),
    path('peliculas/', include('apps.peliculas.urls')),
    path('boletas/', include('apps.boletas.urls')),
    path('salas/', include('apps.salas.urls')),
    path('funciones/', include('apps.funciones.urls')),
    path('select2/', include('django_select2.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
