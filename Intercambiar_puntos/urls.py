from django.urls import path
from . import views

app_name='Intercambiar_puntos' 

urlpatterns=[
    path('seleccionar_categoria/', views.seleccionar_categoria, name='seleccionar_categoria'),
]