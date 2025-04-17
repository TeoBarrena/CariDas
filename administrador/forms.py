from django import forms
from Filiales.models import Filial
import re
from accounts.models import Usuario
class RegistroAyudanteForm (forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese su nombre'}))
    apellido = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese su apellido'}))
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese su DNI'}),max_value=99999999)  # Cambia 'username' por 'dni'
    edad = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese su edad'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'controls','placeholder':'Ingrese su email'}))
    numero = forms.CharField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese su número'}))
    contrasena1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'controls','placeholder':'Elija su contraseña'}))
    contrasena2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'controls','placeholder':'Repita su contraseña'}))
    filial = forms.ModelChoiceField(queryset= Filial.objects.filter(borrado=False, ayudante_id=None), widget=forms.Select(attrs={'class':'controls'}), empty_label="Seleccione una filial")
    foto_perfil = forms.ImageField(label='Seleccione su foto de perfil (opcional)', required=False, widget=forms.FileInput(attrs={'class': 'controls'}))
