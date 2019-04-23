from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('sucursales/', include('apps.sucursales.urls')),
    path('peliculas/', include('apps.peliculas.urls')),
    path('boletas/', include('apps.boletas.urls')),
    path('salas/', include('apps.salas.urls')),
    path('funciones/', include('apps.funciones.urls')),
    path('anuncios/', include('apps.anuncios.urls')),
    path('select2/', include('django_select2.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
