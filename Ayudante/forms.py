from django import forms


class ValidarTicketForm(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese el código del ticket'}),max_value=999999)

    def __init__(self, *args, **kwargs):
        super(ValidarTicketForm, self).__init__(*args, **kwargs)

class CodigoTruequeForm(forms.Form):
    codigo_usuario_trueque = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'controls','placeholder':'Ingrese el código del truequeante'}),max_value=999999)
    codigo_usuario_producto = forms.CharField(widget=forms.TextInput(attrs={'class':'controls','placeholder':'Ingrese el código del que oferto el producto'}))