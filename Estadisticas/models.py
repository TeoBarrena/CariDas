from django.db import models

class Estadisticas(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name