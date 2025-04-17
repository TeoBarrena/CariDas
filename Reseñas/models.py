from django.db import models
from Trueques.models import IntercambioTrueque
from accounts.models import Usuario

# Create your models here.
class Review(models.Model):
    trade = models.ForeignKey(IntercambioTrueque, on_delete=models.CASCADE)
    estrellas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reviews_given')
    user_reseniado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reviews_received')
    realizada = models.BooleanField (default= False)
    def __str__(self):
        return f'Review for {self.trade.title} by {self.user.username}'
