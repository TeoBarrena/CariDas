from datetime import datetime, timezone
from pyexpat.errors import messages
from .forms import ValidarTicketForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth import login
from Caridas import settings
from accounts.models import Usuario
from Trueques.models import Trueque, IntercambioTrueque
from Intercambiar_puntos.models import Ticket
from .forms import CodigoTruequeForm
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

@login_required
def ver_trueques_filial(request):
    # Filtramos los trueques de los usuarios en la misma filial que el usuario actual
    trueques = Trueque.objects.filter(usuario__filial=request.user.filial).exclude(estado_trueque='Eliminado')
    
    if request.method == 'POST':
        trueque_id = request.POST.get('trueque_id')
        try:
            trueque = Trueque.objects.get(id=trueque_id, usuario__filial=request.user.filial)
            
            user_email = trueque.usuario.mail
            send_email_trueque(user_email, trueque)
            trueque.estado_trueque = 'Eliminado' 
            trueque.save()

        except Trueque.DoesNotExist:
            messages.error(request, 'Trueque no encontrado.')
    
    return render(request, 'ver_trueques_filial.html', {'trueques': trueques})

@login_required
def validar_ticket_usuario(request):
    if request.method == 'GET':
        form = ValidarTicketForm()
    else:    
        if request.method == 'POST':
            form = ValidarTicketForm(request.POST)
            if form.is_valid():
                codigo = form.cleaned_data['codigo']
                try:
                    ticket = Ticket.objects.get(codigo=codigo)
                    # Check for ticket expiration using datetime objects
                    if ticket.fecha_caducidad < datetime.now().date():
                        return render(request, 'validar_ticket_usuario.html', {'form':form,'Error_fecha': True})
                    else:
                        categoria = ticket.categoria
                        ticket.delete()
                        return render(request, 'validar_ticket_usuario.html', {'form':form,'categoria': categoria})
                except Ticket.DoesNotExist:
                    return render(request, 'validar_ticket_usuario.html', {'form':form,'error': True})
    return render(request, 'validar_ticket_usuario.html',{'form':form})

def enviar_codigo(request):
    codigo_generado = request.session.get('codigo_generado')
    user_id = request.session.get('user_id') #anda bien
    user = Usuario.objects.get(id= user_id)
    mail = request.session.get('mail') #anda bien
    send_email(mail, codigo_generado) #send_email tendria que estar en views.py de accounts y se podria hacer un send_email_usuario y send_email_ayudante porque son distintos
    if request.method == 'POST':
        numero_ingresado = request.POST.get('codigo')#obtiene el numero que esta en el campo codigo
        if str(numero_ingresado) != str(codigo_generado):
            next_url = request.session.get('next_url')
            if next_url != None:
                return redirect(next_url)
            return render(request, 'enviar_codigo.html', {'mail': mail, 'error_codigo_ingresado':True})
        else:
            login(request, user)
            return redirect('Pantalla_principal:Pantalla_principal')
    return render(request, 'enviar_codigo.html', {'mail': mail})
    
def send_email(mail,numero):
    context = {'numero':numero, 'mostrar_codigo':True}
    template = get_template('correo.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Codigo de validacion de inicio de sesion como ayudante', #titulo que le aparece en el mail
        'no se que sentido tiene esto, pero va',
        settings.EMAIL_HOST_USER, #desde que cuenta se manda
        [mail], #esto es a quien se lo mande
    )
    email.attach_alternative(content, 'text/html')
    email.send()

@login_required
#se podria agregar la verificacion de que is_ayudante = True o 1 no me acuerdo
def vista_ayudante(request):
    return render(request,'vista_ayudante.html')

def send_email_trueque(mail, trueque):
    context = {'trueque': trueque}
    template = get_template('trueque_eliminado.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Trueque Eliminado',  # Asunto del correo
        'Su Trueque ha sido eliminado.',  # Cuerpo del correo en texto plano
        settings.EMAIL_HOST_USER,  # Desde qué cuenta se manda
        [mail],  # A quién se envía el correo
    )
    email.attach_alternative(content, 'text/html')
    email.send()


def send_email_trueque(mail, trueque):
    context = {'trueque': trueque}
    template = get_template('trueque_eliminado.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Trueque Eliminado',  # Asunto del correo
        'Su Trueque ha sido eliminado.',  # Cuerpo del correo en texto plano
        settings.EMAIL_HOST_USER,  # Desde qué cuenta se manda
        [mail],  # A quién se envía el correo
    )
    email.attach_alternative(content, 'text/html')
    email.send()

@login_required
def validar_codigo_trueque(request):
    if request.method == 'POST':
        form = CodigoTruequeForm(request.POST)
        if form.is_valid():
            codigo_usuario_trueque = form.cleaned_data['codigo_usuario_trueque']
            codigo_usuario_producto = form.cleaned_data['codigo_usuario_producto']
            dia_actual = date.today()
            filial = request.user.filial
            try:
                intercambio = IntercambioTrueque.objects.get(codigo_usuario_trueque = codigo_usuario_trueque, codigo_usuario_producto = codigo_usuario_producto)
                if intercambio.turno.dia == dia_actual:
                    #tira el error del dia
                    if intercambio.turno.filial == filial:
                        #tira el error de la filial
                        intercambio.estado = 'Completado'
                        intercambio.trueque_1.usuario.puntos += intercambio.trueque_1.categoria.puntos/4
                        
                        intercambio.fue_trueque = True
                        intercambio.trueque_1.usuario.save()# Guardar los cambios en el usuario de trueque_1
                        intercambio.producto_2.usuario.puntos += intercambio.producto_2.categoria.puntos/4
                        intercambio.fue_producto = True
                        intercambio.producto_2.usuario.save()# Guardar los cambios en el usuario de producto_2
                        intercambio.save()
                        return render(request, 'validar_codigo_trueque.html',{'form':form, 'trueque_completado':True})
                    else:
                        return render(request, 'validar_codigo_trueque.html',{'form':form, 'error_filial':True})
                else:
                    return render(request, 'validar_codigo_trueque.html',{'form':form, 'error_dia':True})
            except:
                return render(request, 'validar_codigo_trueque.html',{'form':form, 'error':True})
    else:
        form = CodigoTruequeForm()
    return render(request, 'validar_codigo_trueque.html', {'form': form})

@login_required
def permitir_trueque(request):
    error = None

    if request.method == 'POST':
        dni = request.POST.get('dni')
        codigo = request.POST.get('codigo')
        dia_actual = date.today()

        # Detectar el tipo de usuario basado en el código
        if codigo.isdigit():
            tipo_usuario = 'creador'
        else:
            tipo_usuario = 'ofertante'

        try:
            usuario = Usuario.objects.get(dni=dni)
            if tipo_usuario == 'creador':
                intercambios = IntercambioTrueque.objects.filter(trueque_1__usuario=usuario, turno__dia=dia_actual, fue_trueque=False, codigo_usuario_trueque=codigo)
                if intercambios.exists():
                    for intercambio in intercambios:
                        intercambio.fue_trueque = True
                        intercambio.estado = 'Rechazado'
                        intercambio.save()
                else:
                    error = "No se encontró un intercambio pendiente en el día actual con ese código."
            elif tipo_usuario == 'ofertante':
                intercambios = IntercambioTrueque.objects.filter(producto_2__usuario=usuario, turno__dia=dia_actual, fue_producto=False, codigo_usuario_producto=codigo)
                if intercambios.exists():
                    for intercambio in intercambios:
                        intercambio.fue_producto = True
                        intercambio.estado = 'Rechazado'
                        intercambio.save()
                else:
                    error = "No se encontró un intercambio pendiente en el día actual con ese código."
            else:
                error = "Tipo de usuario no válido."

            if not error:
                render(request, 'permitir_trueque.html', {'error': error})

        except Usuario.DoesNotExist:
            error = "El DNI ingresado no se encuentra registrado en el sistema."
    
    return render(request, 'permitir_trueque.html', {'error': error})