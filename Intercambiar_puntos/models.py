from django.db import models
from Productos.models import Categoria
# Create your models here.
class Ticket(models.Model):
    codigo = models.IntegerField(unique=True)
    fecha_caducidad = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
