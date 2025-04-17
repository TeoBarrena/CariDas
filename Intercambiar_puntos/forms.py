from django import forms
from Filiales.models import Filial
import re
from Productos.models import Categoria

class SeleccionarCategoriaForm(forms.Form):
    categoria = forms.ModelChoiceField(queryset= Categoria.objects.filter(borrado=False), widget=forms.Select(attrs={'class':'controls'}), empty_label="Seleccione una categoria")
