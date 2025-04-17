from django.urls import path
from . import views

app_name = 'Trueques'

urlpatterns = [
    path('registro_trueque/', views.registro_trueque, name='registro_trueque'),
    path('trueques_aceptados/', views.trueques_en_espera_de_confirmacion, name='ver_trueques_en_espera_de_confirmacion'),
    path('ofertar_producto/', views.ofertar_producto, name='ofertar_producto'),
    path('almacenar_trueque/<int:trueque_id>/', views.almacenar_trueque_id, name='almacenar_trueque'),
    path('procesar_oferta/', views.procesar_oferta, name='procesar_oferta'),
    path('cancelar_trueque/<int:trueque_id>/', views.cancelar_trueque, name='cancelar_trueque'),
]