from django.urls import path
from . import views

app_name='busqueda'

urlpatterns = [
    path('trueques_usuarios/', views.listar_trueques, name='listar_Trueques'),
]
