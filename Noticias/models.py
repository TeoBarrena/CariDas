from django.db import models

class Noticia(models.Model):
  titulo = models.CharField(max_length=200)
  descripcion = models.TextField()
  foto = models.ImageField(upload_to='', null=True)
  borrado = models.BooleanField(default=False)
  fecha_creado = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.titulo
