from django.shortcuts import render
from .forms import SeleccionarCategoriaForm
from django.contrib.auth.decorators import login_required
from .models import Ticket
import random
from datetime import timedelta
from django.utils import timezone
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# Create your views here.

@login_required
def seleccionar_categoria(request):
    usuario = request.user
    puntos_usuario = usuario.puntos # anda bien, obtiene los puntos del usuario
    form = SeleccionarCategoriaForm()
    if request.method == 'POST':
        form = SeleccionarCategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.cleaned_data['categoria']
            if puntos_usuario < categoria.puntos:
                return render(request,'seleccionar_categoria.html',{'form': form, 'puntos_usuario':puntos_usuario,'error_puntos':True,'puntos_necesarios':categoria.puntos})
            else:
                usuario.puntos -= categoria.puntos
                usuario.save()
                codigo = random.randint(100000,999999)
                #para hacer que el codigo sea unico y no se repitan codigos 
                while Ticket.objects.filter(codigo=codigo).exists():
                    codigo = random.randint(100000,999999)
                fecha_caducidad = timezone.now() + timedelta(days=31)
                ticket = Ticket(
                    codigo = codigo,
                    fecha_caducidad = fecha_caducidad,
                    categoria = categoria
                )
                ticket.save()
                send_email(usuario.mail,codigo,fecha_caducidad,categoria)
                return render(request, 'seleccionar_categoria.html', {'form': form, 'puntos_usuario': usuario.puntos, 'intercambio_exitoso': True})
    return render(request, 'seleccionar_categoria.html', {'form': form, 'puntos_usuario': puntos_usuario})

def send_email(mail,codigo,fecha_caducidad,categoria):

    context = {'codigo':codigo, 'fecha_caducidad':fecha_caducidad, 'categoria':categoria}
    
    template = get_template('correoTicket.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Ticket para intercambiar por producto', #titulo que le aparece en el mail
        'no se que sentido tiene esto, pero va',
        settings.EMAIL_HOST_USER, #desde que cuenta se manda
        [mail], #esto es a quien se lo mande
    )
    email.attach_alternative(content, 'text/html')
    email.send()