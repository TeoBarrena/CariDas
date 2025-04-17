from django.urls import path
from . import views

app_name='Noticias'

urlpatterns=[
    path('agregar_noticia/', views.agregar_noticia,name="agregar_noticia"),
    path('delete_noticia/', views.delete_noticia,name="delete_noticia"),
    path('modify_noticia/', views.modify_noticia,name="modify_noticia"),
    path('set_noticia_id/', views.set_noticia_id, name="set_noticia_id"),
    ]
