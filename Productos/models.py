from django.db import models
from accounts.models import Usuario,Filial

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=15, unique=True)
    puntos = models.IntegerField(default=100)
    borrado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ESTADO_OPCIONES = [('nuevo', 'Nuevo'), ('usado - como nuevo', 'Usado - Como nuevo'), ('usado - muy bueno', 'Usado - Muy bueno'),('usado - bueno', 'Usado - Bueno'),('usado - aceptable', 'Usado - Aceptable')]
    titulo = models.CharField(max_length=15) 
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES,
        default='Nuevo',)
    foto_producto = models.ImageField(upload_to='media/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='productos')
    borrado = models.BooleanField(default=False)
    motivo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo