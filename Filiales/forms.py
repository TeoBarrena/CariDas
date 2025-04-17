from django import forms
from .models import Filial

class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ['nombre', 'direccion']
    
    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if Filial.objects.filter(direccion=direccion).exists():
            raise forms.ValidationError('Ya existe una filial con esta direccion')
        return direccion