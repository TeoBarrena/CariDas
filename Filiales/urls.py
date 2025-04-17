from django.urls import path
from . import views

app_name = 'Filiales'
app_name = 'Filiales'

urlpatterns = [
    path('create_filial/', views.create_filial, name="create_filial"),
    path('list_filiales/', views.list_filiales, name="list_filiales"),
    path('modify_filial/', views.modify_filial, name="modify_filial"),
    path('set_filial_id/<int:filial_id>/', views.set_filial_id, name="set_filial_id"),
    path('ver_datos_filiales/', views.ver_datos_filiales, name='ver_datos_filiales'),
    path('select_filial/', views.select_filial, name="select_filial"),
]
