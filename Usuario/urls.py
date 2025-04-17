from django.urls import path
from . import views

app_name='Usuario' #esto es necesario para que dps cuando va a reest. contraseña o reg. usuario, siga el link apropiado

#urls que los clientes pueden visitar
urlpatterns = [
    path('opciones_trueque/', views.opciones_trueque,name="opciones_trueque"),
    path('productos/', views.show_productos, name='show_productos_usuario'),
    path('trueques/', views.show_trueques, name='show_trueques_usuario'),
    path('opciones_trueque/', views.opciones_trueque, name='opciones_trueque'),
    
]
