from django.urls import path
from . import views

app_name='Ayudante'

urlpatterns=[
    path('enviar_codigo/', views.enviar_codigo, name="enviar_codigo"),
    path('vista_ayudante/', views.vista_ayudante, name="vista_ayudante"),
    path('trueques_filial/', views.ver_trueques_filial, name="Ver_Trueques_filial"),
    path('validar_ticket/', views.validar_ticket_usuario, name="Validar_ticket_usuario"),
    path('validar_codigo_trueque/', views.validar_codigo_trueque, name='validar_codigo_trueque'),
    path('permitir_trueque/', views.permitir_trueque, name='permitir_trueque'),
]