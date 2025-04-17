from django.db import models
from django.contrib.auth.models import AbstractUser
from Filiales.models import Filial

class StarRating(models.IntegerChoices):
    ONE_STAR = 1, '1 Star'
    TWO_STARS = 2, '2 Stars'
    THREE_STARS = 3, '3 Stars'
    FOUR_STARS = 4, '4 Stars'
    FIVE_STARS = 5, '5 Stars'

# Create your models here.
class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    dni = models.CharField(max_length=10, unique=True, null=True)
    age = models.IntegerField()
    mail = models.EmailField()
    num = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='media/', null=True, blank=True)
    first_name = models.CharField(max_length=30, default="sin_nombre")
    last_name = models.CharField(max_length=30)
    blocked = models.BooleanField(default=False)
    is_ayudante = models.BooleanField(default=False)
    filial = models.ForeignKey('Filiales.Filial', on_delete=models.SET_NULL, null=True, blank=True)
    puntos = models.IntegerField(default=100)
    estrellas = models.IntegerField(choices=StarRating.choices, default=StarRating.FIVE_STARS)
    USERNAME_FIELD = 'dni'
    cant_resenias = models.IntegerField(default=1)
    estrellas_totales =  models.IntegerField (default=5)

    
