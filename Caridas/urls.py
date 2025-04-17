from django.contrib import admin
from django.urls import path,include
from administrador import views as admin_views
from django.conf import settings
from django.conf.urls.static import static

#urls que los clientes pueden visitar
urlpatterns = [
    path('admin/', admin.site.urls), #aca en vez de llamar a admin.site.urls podria llamar al html correspondiente 
    path('productos/', include('Productos.urls')),
    path('filiales/', include('Filiales.urls')),    
    path('accounts/', include('accounts.urls')),  
    path('', include('Pantalla_principal.urls')),
    path('administrador/', include('administrador.urls')),
    path('ayudante/', include('Ayudante.urls')),
    path('usuario/', include('Usuario.urls')),
    path('busqueda/', include('busqueda.urls')),
    path('Intercambiar_puntos/', include('Intercambiar_puntos.urls')),
    path('Trueques/', include('Trueques.urls')),
    path('Noticias/', include('Noticias.urls')),
    path('Reseñas/', include('Reseñas.urls')),
    path('Donaciones/', include('Donaciones.urls')),
    path('Estadisticas/', include('Estadisticas.urls')),
]

handler404 = admin_views.error404
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
