from django.urls import path
from . import views

app_name = 'Reseñas'

urlpatterns = [
    path('add_review/<int:trade_id>/', views.add_review, name='add_review'),
]