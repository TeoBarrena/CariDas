# administrador/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('listado/', views.seleccionar, name='seleccionar'),
    path('usuarios/', views.show_usuarios, name='show_usuarios'),
    path('productos/', views.show_productos, name='show_productos'),
    path('trueques/', views.show_trueques, name='show_trueques'),
    path('registrar_ayudante/', views.registrar_ayudante, name='registrar_ayudante'),
    path('vista_admin/', views.vista_admin, name='vista_admin'),
    path('editar_perfil_admin/', views.editar_perfil, name='editar_perfil_admin'),
    path('ver_perfil/<int:user_id>/', views.ver_perfil, name='ver_perfil'),
    path('error404/', views.error404, name='error404'),
]