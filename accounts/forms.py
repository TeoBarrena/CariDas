#script para crear formulario para el registro de los usuarios
from django import forms
from Filiales.models import Filial

class RegistroUsuarioForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese su nombre'}))
    apellido = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese su apellido'}))
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese su DNI'}),max_value=99999999)  # Cambia 'username' por 'dni'
    edad = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese su edad'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'controls','placeholder':'Ingrese su email'}))
    numero = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese su número de celular'}))
    contrasena1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'controls','placeholder':'Elija su contraseña'}))
    contrasena2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'controls','placeholder':'Repita su contraseña'}))
    foto_perfil = forms.ImageField(label='Seleccione su foto de perfil (opcional)', required=False, widget=forms.FileInput(attrs={'class': 'controls'}))
    filial = forms.ModelChoiceField(queryset= Filial.objects.all(), widget=forms.Select(attrs={'class':'controls'}), empty_label="Seleccione una filial")

    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
    
class LoginForm(forms.Form):
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'username','placeholder':'Ingrese su dni'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password','placeholder':'Ingrese su contraseña'}))#script para crear formulario para el registro de los usuarios
