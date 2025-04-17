from django.db import models
from Productos.models import Producto, Categoria
from accounts.models import Usuario
from django.core.exceptions import ValidationError
from Filiales.models import Filial

class Trueque(models.Model):
    titulo = models.CharField(max_length=100)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ESTADO_OPCIONES = [('nuevo', 'Nuevo'), ('usado - como nuevo', 'Usado - Como nuevo'), ('usado - muy bueno', 'Usado - Muy bueno'),('usado - bueno', 'Usado - Bueno'),('usado - aceptable', 'Usado - Aceptable')]
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES,
        default='Nuevo',)
    descripcion = models.TextField(max_length=500)
    foto_producto = models.ImageField(upload_to='media/', blank=True, null=True)
    foto_producto = models.ImageField(upload_to='media/', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='trueques')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    ESTADO_TRUEQUE = [('Pendiente', 'Pendiente'), ('Aceptado','Aceptado'),('Rechazado', 'Rechazado'),('Eliminado','Eliminado'),('Completado','Completado')]
    estado_trueque = models.CharField(max_length=20, choices=ESTADO_TRUEQUE, default='Pendiente')
    
    
    def __str__(self):
        return self.titulo
    
class Turno(models.Model):
    dia = models.DateField()
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='turno')
    fecha_creado = models.DateTimeField(auto_now_add=True)
    

class IntercambioTrueque(models.Model):
    trueque_1 = models.ForeignKey(Trueque, on_delete=models.CASCADE, related_name='intercambio_1')
    producto_2 = models.ForeignKey(Producto, on_delete=models.CASCADE,related_name='producto_2')
    codigo_usuario_trueque = models.IntegerField(default=0)
    codigo_usuario_producto = models.CharField(max_length=20,default='')
    producto_2 = models.ForeignKey(Producto, on_delete=models.CASCADE,related_name='producto_2')
    codigo_usuario_trueque = models.IntegerField(default=0)
    codigo_usuario_producto = models.CharField(max_length=20,default='')
    ESTADO_INTERCAMBIO = [
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('Completado', 'Completado'),
        ('Rechazado', 'Rechazado'),
        ('Espera de confirmacion','Espera de confirmacion'),
        ('Espera de confirmacion','Espera de confirmacion'),
        ('Eliminado','Eliminado')
    ]
    estado = models.CharField(max_length=30, choices=ESTADO_INTERCAMBIO, default='Espera de confirmacion')
    estado = models.CharField(max_length=30, choices=ESTADO_INTERCAMBIO, default='Espera de confirmacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    turno = models.ForeignKey(Turno, null=True, blank=True, on_delete=models.SET_NULL)
    fue_trueque = models.BooleanField (default= False)
    fue_producto = models.BooleanField (default= False)

    def __str__(self):
        return f"Intercambio entre {self.trueque_1.usuario} y {self.producto_2.usuario}"
    
    def __id__(self):
        return self.id
    
    def __id__(self):
        return self.id

    def clean(self):
        # Validar que los usuarios son diferentes
        if self.trueque_1.usuario == self.producto_2.usuario:
            raise ValidationError('El intercambio no puede ser realizado entre el mismo usuario.')
        # Validar que los productos son diferentes
        if self.trueque_1.producto == self.producto_2.titulo:
            raise ValidationError('El intercambio no puede ser realizado con el mismo producto.')



