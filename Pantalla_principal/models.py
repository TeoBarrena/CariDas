from django.db import models
from accounts.models import Usuario

# Create your models here.
class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    borrado = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.usuario.username} - {self.mensaje[:20]}"