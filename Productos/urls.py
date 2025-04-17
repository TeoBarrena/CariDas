from django.urls import path
from . import views

app_name='Productos' #esto es necesario para que dps cuando va a reest. contraseña o reg. usuario, siga el link apropiado

#urls que los clientes pueden visitar
urlpatterns = [
    path('create_category/', views.create_category,name="create_category"),
    path('create_product/', views.create_product,name="create_product"),
    path('delete_category/', views.delete_category,name="delete_category"),
    path('list_category/', views.list_category,name="list_category"),]
