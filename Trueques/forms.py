from django import forms
from .models import Trueque
from Productos.models import Producto, Categoria
from .models import Turno
from .models import Turno

class TruequeForm(forms.Form):
    titulo = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese el titulo'}))
    descripcion = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'controls','placeholder':'Ingrese la descripcion'}))
    #estado = forms.ChoiceField(
    #    choices= Trueque.ESTADO_OPCIONES,
    #    widget=forms.Select(attrs={'class':'controls'})
    #)
    #categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(borrado=False), empty_label="Selecciona una categoria")
    #categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(borrado=False), empty_label="Selecciona una categoria")
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),  # Inicialmente vacío
        empty_label="Selecciona un producto"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TruequeForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['producto'].queryset = Producto.objects.filter(usuario=user, borrado = False)


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['dia']
    
    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        # Limitamos la selección solo a sábados y domingos
        self.fields['dia'].widget = forms.SelectDateWidget()
        self.fields['dia'].widget.attrs.update({'type': 'date'})
        
    def clean_dia(self):
        dia = self.cleaned_data['dia']
        if dia.weekday() not in [5, 6]:  # 5 = sábado, 6 = domingo
            raise forms.ValidationError("Solo puedes seleccionar sábados y domingos.")
        if Turno.objects.filter(dia=dia).count() >= 50:
            raise forms.ValidationError("Ya no hay turnos disponibles para este día.")
        return dia


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['dia']
    
    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        # Limitamos la selección solo a sábados y domingos
        self.fields['dia'].widget = forms.SelectDateWidget()
        self.fields['dia'].widget.attrs.update({'type': 'date'})
        
    def clean_dia(self):
        dia = self.cleaned_data['dia']
        if dia.weekday() not in [5, 6]:  # 5 = sábado, 6 = domingo
            raise forms.ValidationError("Solo puedes seleccionar sábados y domingos.")
        if Turno.objects.filter(dia=dia).count() >= 50:
            raise forms.ValidationError("Ya no hay turnos disponibles para este día.")
        return dia