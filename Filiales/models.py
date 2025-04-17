from django.db import models

# Create your models here.
class Filial(models.Model):
    nombre = models.CharField(max_length=150, unique=False, null=True, blank=True)
    direccion = models.CharField(max_length=100, unique=True)
    ayudante = models.ForeignKey('accounts.Usuario', on_delete=models.SET_NULL, null=True, related_name='filiales_ayudadas')
    borrado = models.BooleanField(default=False)

    def __str__(self):
        return self.direccion