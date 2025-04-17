from django import forms
from .models import Review

class ReviewForm(forms.Form):
    estrellas = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        label="Selecciona la cantidad de estrellas",
        widget=forms.Select
    )
    comentario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese el comentario'}))