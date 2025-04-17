from django import forms
from .models import Categoria, Producto
from spanlp.palabrota import Palabrota

class CategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese el nombre'}))
    puntos = forms.IntegerField(widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese los puntos para la categoria'}))
    
class ProductForm(forms.Form):
    titulo = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese el titulo'}))
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'controls','placeholder':'Ingrese la descripcion'}))
    estado = forms.ChoiceField(
        choices= Producto.ESTADO_OPCIONES,
        widget=forms.Select(attrs={'class':'controls'})
    )
    categoria = forms.ChoiceField(
        choices=[],  # Se llenarán dinámicamente en el método __init__
        widget=forms.Select(attrs={'class':'controls'})
    )
    foto_producto = forms.ImageField(label='Seleccione la foto del producto', widget=forms.FileInput(attrs={'class': 'controls'}))

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        categorias = Categoria.objects.filter(borrado=False)
        self.fields['categoria'].choices = [(categoria.id, categoria.nombre) for categoria in categorias]

  
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')

        badWords = Palabrota()
        contain_badWords = badWords.contains_palabrota(descripcion)

        if (contain_badWords):
            print('bloquear usuario')
            #MANDAR EL USUARIO AL INICIO 
            #SUBIR EL USUARIO A LA TABLA DE BLOQUEADOS DE LA BASE DE DATOS

        return descripcion