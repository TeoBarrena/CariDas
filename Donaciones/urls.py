from django.urls import path
from . import views

app_name = 'Donaciones'

urlpatterns = [
    path('donar/', views.donar, name='donar'),
]