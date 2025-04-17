from django.urls import path
from . import views

app_name='accounts' #esto es necesario para que dps cuando va a reest. contraseña o reg. usuario, siga el link apropiado

urlpatterns=[
    path('login/', views.signin, name='login'),

    path('reestablecer_contrasena/', views.reestablecer_contrasena,name="reestablecer_contrasena"),
    path('verificar_codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('cambiar_contrasena/',views.cambiar_contrasena,name='cambiar_contraseña'),

    path('registrar_usuario/', views.registrar_usuario,name="registrar_usuario"),
    
    path('login/logout', views.cerrar_sesion, name='logout'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    ]
