from django.urls import path
from . import views

app_name='Pantalla_principal' #esto es necesario para que dps cuando va a reest. contraseña o reg. usuario, siga el link apropiado

#urls que los clientes pueden visitar
urlpatterns = [
    path('', views.pantalla_principal,name="Pantalla_principal"),
    path('listar_notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    path('delete_notificacion/', views.delete_notificacion, name='delete_notificacion'),
    path('donaciones/', views.donaciones,name="Donaciones"),
]
