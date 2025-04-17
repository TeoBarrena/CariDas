from django.urls import path
from .views import view_statistics, estadisticas_pdf

app_name = 'Estadisticas'

urlpatterns = [
    path('view_statistics/', view_statistics, name='view_statistics'),
    path('pdf/', estadisticas_pdf, name='estadisticas_pdf'),
]
