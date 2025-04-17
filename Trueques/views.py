from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TruequeForm
from .models import Producto, Trueque,IntercambioTrueque
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
import logging
from django.db.models import Q
import random
import string
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from .models import Turno
from datetime import date, timedelta
from Pantalla_principal.models import Notificacion


@login_required
def registro_trueque(request):
    productos_disponibles = Producto.objects.filter(usuario=request.user, borrado=False)
    if not productos_disponibles.exists():
        return render(request, 'registro_trueque.html', {'sin_productos': True})
    if request.method == 'POST':
        #verificar maximo 5 trueques en estado pendiente
        form = TruequeForm(request.POST, user = request.user)
        if form.is_valid():
            user = request.user
            if (user.estrellas < 3):
                return render(request, 'registro_trueque.html', {'form': form, 'error_estrellas':True})
            #verifica que la cantidad de trueques en estado pendiente no sean 5
            if Trueque.objects.filter(usuario=request.user, estado_trueque='Pendiente').count() == 5:
                return render(request, 'registro_trueque.html', {'form': form, 'max_trueques_pendientes':True})
            else:
                #verifica que el producto no este cargado en otro trueque que este pendiente 
                producto = form.cleaned_data['producto']
                if Trueque.objects.filter(usuario=request.user,estado_trueque='Pendiente',producto = producto):
                    return render(request, 'registro_trueque.html', {'form': form, 'producto_ya_cargado':True})
                else:
                    trueque = Trueque(titulo=form.cleaned_data['titulo'], producto=producto,
                                    estado=producto.estado, descripcion=form.cleaned_data['descripcion'],
                                    foto_producto=producto.foto_producto, usuario = request.user, categoria=producto.categoria, )
                    trueque.save()
                    messages.success(request, 'Trueque registrado exitosamente.')
                    return redirect('Usuario:show_trueques_usuario')
    else:
        form = TruequeForm(user=request.user)
    return render(request, 'registro_trueque.html', {'form': form})

@login_required
def historial_trueques_usuario(request):
    user_trueques = Trueque.objects.filter(usuario=request.user)
    accepted_trueques = user_trueques.filter(estado_trueque='Aceptado')
    canceled_trueques = user_trueques.filter(estado_trueque='Cancelado')
    pending_trueques = user_trueques.filter(estado_trueque='Pendiente')

    print(accepted_trueques)
    print(canceled_trueques)
    print(pending_trueques)

    return render(request, 'historial_trueques_usuario.html', {
        'accepted_trueques': accepted_trueques,
        'canceled_trueques': canceled_trueques,
        'pending_trueques': pending_trueques,
    })

@login_required
def cancelar_trueque(request, trueque_id):
    trueque = Trueque.objects.get(id=trueque_id)
    trueque.estado_trueque = 'Cancelado'
    trueque.save()
    return redirect('Usuario:show_trueques_usuario')
@login_required
def almacenar_trueque_id(request, trueque_id):
    request.session['trueque_id'] = trueque_id
    return redirect('Trueques:ofertar_producto')

@login_required
def ofertar_producto(request):
    trueque_id = request.session.get('trueque_id')#obtiene el id del trueque, el que esta a la izqueirda
    if trueque_id is None:
        # Manejar el caso en que no se encuentra el trueque_id en la sesión
        return redirect('busqueda:listar_Trueques')  # Redirigir a la lista de trueques o a otra vista

    trueque = get_object_or_404(Trueque, id=trueque_id)#aca obtiene el trueque ofertado, el que esta a la izquierda
    categoria = trueque.producto.categoria
    #para obtener los productos del que va a ofertar algun producto (los que estan a la derecha)
    productos_del_usuario = Producto.objects.filter(usuario=request.user, categoria=categoria, borrado=False)
    #verifica si el usuario que quiere ofertar algun rpodcuto no tiene ningun producot cargado en esa categoria
    if not productos_del_usuario.exists():
        return render(request, 'trueque.html', {'trueque': trueque,'productos_del_usuario': productos_del_usuario, 'vacio':True})    
    
    return render(request, 'trueque.html', {'trueque': trueque,'productos_del_usuario': productos_del_usuario})

logger = logging.getLogger(__name__)

@csrf_exempt
def procesar_oferta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id') # el producto de la derecha
        trueque_id = data.get('trueque_id') # el de la izquierda

        if producto_id and trueque_id:
            trueque_1 = get_object_or_404(Trueque, id=trueque_id)
            producto_2 = get_object_or_404(Producto, id=producto_id)

            try:
                # Verifica si ya existe un intercambio entre estos trueques
                if IntercambioTrueque.objects.filter(
                    Q(trueque_1=trueque_1, producto_2=producto_2) |
                    Q(producto_2=producto_2, trueque_1=trueque_1)
                ).exists():
                    raise ValidationError('El intercambio entre estos trueques ya existe.')

                # Si no existe, crea el intercambio y lo notifica al usuario creador
                mensaje_trueque = f"Tu trueque '{trueque_1.titulo}' ha recibido una solicitud."
                notificacion_trueque = Notificacion(usuario=trueque_1.usuario, mensaje=mensaje_trueque)
                notificacion_trueque.save()

                intercambio = IntercambioTrueque(
                    trueque_1=trueque_1,
                    producto_2=producto_2,
                    codigo_usuario_trueque = 0,
                    codigo_usuario_producto = 0
                )
                intercambio.full_clean()  # Usa full_clean para validar el modelo
                intercambio.save()
                return JsonResponse({'success': True})
            except ValidationError as e:
                # Imprime el error exacto en la consola para depuración
                print(e)
                return JsonResponse({'success': False, 'error': e.messages})
            except Exception as e:
                # Imprime el error exacto en la consola para depuración
                print(e)
                return JsonResponse({'success': False, 'error': 'Error al crear el intercambio.'})
        else:
            return JsonResponse({'success': False, 'error': 'Datos inválidos.'})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})


def generar_codigo_random_usuario_trueque():
    codigo = ''.join(random.choices(string.digits, k=6))
    return codigo

def generar_codigo_random_usuario_producto():
    codigo = ''.join(random.choices(string.ascii_letters, k=6))
    return codigo

def send_mail_usuario_producto(mail, codigo_usuario_producto, dia, filial):
    context = {
        'codigo': codigo_usuario_producto,
        'dia': dia,
        'filial': filial
    }
    template = get_template('correo_usuario_trueque.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Codigo generado por el trueque que ofertaste', #titulo que le aparece en el mail
        'no se que sentido tiene esto, pero va',
        settings.EMAIL_HOST_USER, #desde que cuenta se manda
        [mail], #esto es a quien se lo mande
    )
    email.attach_alternative(content, 'text/html')
    email.send()

def send_mail_usuario_trueque(mail, codigo_usuario_trueque, dia, filial):
    context = {
        'codigo': codigo_usuario_trueque,
        'dia': dia,
        'filial': filial
    }
    template = get_template('correo_usuario_trueque.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Codigo generado por el trueque que ofertaste', #titulo que le aparece en el mail
        'no se que sentido tiene esto, pero va',
        settings.EMAIL_HOST_USER, #desde que cuenta se manda
        [mail], #esto es a quien se lo mande
    )
    email.attach_alternative(content, 'text/html')
    email.send()

#recibe por parametro un objeto de tipo IntercambioTrueque
#anda bien
def notificar_trueque_aceptado(trueque):
    #esto notifica al que publico el trueque
    mensaje_trueque = f"Aceptaste el trueque '{trueque.trueque_1.titulo}' a cambio del producto {trueque.producto_2.titulo}."
    notificacion_trueque = Notificacion(usuario=trueque.trueque_1.usuario, mensaje=mensaje_trueque)
    notificacion_trueque.save()

    #esto notifica al que oferto un producto
    mensaje_trueque = f"El producto '{trueque.producto_2.titulo}' que ofertaste en el trueque '{trueque.trueque_1.titulo}' fue aceptado'."
    notificacion_trueque = Notificacion(usuario=trueque.producto_2.usuario, mensaje=mensaje_trueque)
    notificacion_trueque.save()

    #notificar a los otros usuarios que realizaron la oferta de un producto para el trueque diciendo que eligio otra oferta
    otros_trueques = IntercambioTrueque.objects.filter(
        trueque_1=trueque.trueque_1,
        estado__in=['Rechazado']
    ).exclude(id=trueque.id)
    for otro_trueque in otros_trueques:
        mensaje_otro_usuario = f"Tu oferta para el trueque '{trueque.trueque_1.titulo}' con el producto '{otro_trueque.producto_2.titulo}' no fue aceptada. Se eligió otra oferta."
        notificacion_otro_usuario = Notificacion(usuario=otro_trueque.producto_2.usuario, mensaje=mensaje_otro_usuario)
        notificacion_otro_usuario.save()

@login_required
def trueques_en_espera_de_confirmacion(request):
    intercambios = IntercambioTrueque.objects.filter(trueque_1__usuario = request.user.id, estado='Espera de confirmacion')
    error_message = None

    if request.method =='POST':
        action = request.POST.get('action')
        intercambio_id = request.POST.get('intercambio_id')
        motivo_rechazo = request.POST.get('motivo_rechazo', '') 
        try:
            intercambio = IntercambioTrueque.objects.get(pk=intercambio_id)
        except IntercambioTrueque.DoesNotExist:
            error_message = "El intercambio no existe."
            return render(request, 'trueques_en_espera_de_confirmacion.html', {'intercambios': intercambios, 'error': error_message})

        #el dueño del trueque acepta el producto ofertado
        if action == 'aceptar':
            turno_dia = buscar_proximo_turno_disponible(intercambio.trueque_1.usuario.filial)
            if not turno_dia:
                error_message = 'No hay cupos disponibles.'
                return render(request, 'trueques_en_espera_de_confirmacion.html', {'intercambios': intercambios,'error': error_message})


            turno = Turno.objects.create(dia=turno_dia, filial=intercambio.trueque_1.usuario.filial, usuario=request.user)

            intercambio.estado = 'Aceptado'
            intercambio.trueque_1.estado_trueque = 'Aceptado'
            intercambio.turno = turno
            intercambio.trueque_1.save()

            # Encuentra y actualiza todos los intercambios con el mismo trueque_1_id excepto el actual
            otros_intercambios_mismo_trueque = IntercambioTrueque.objects.filter(trueque_1=intercambio.trueque_1).exclude(pk=intercambio_id)
            for inter in otros_intercambios_mismo_trueque:
                inter.estado = 'Rechazado'
                inter.trueque_1.estado_trueque = 'Rechazado'
                inter.save()

            # Encuentra y actualiza todos los intercambios con el mismo producto_2
            intercambios_mismo_producto = IntercambioTrueque.objects.filter(producto_2_id=intercambio.producto_2)
            for inter in intercambios_mismo_producto:
                inter.estado = 'Rechazado'
                inter.trueque_1.estado_trueque = 'rechazado'
                inter.save()

            #genera el codigo para el q oferto el trueque
            codigo_usuario_trueque = generar_codigo_random_usuario_trueque()
            #genera el codigo para el q oferto algun producto suyo
            codigo_usuario_producto = generar_codigo_random_usuario_producto()
        

            #los guarda en la base de datos 
            intercambio.codigo_usuario_trueque = codigo_usuario_trueque
            intercambio.codigo_usuario_producto = codigo_usuario_producto
            #les mande el mail a cada uno
            send_mail_usuario_trueque(intercambio.trueque_1.usuario.mail,codigo_usuario_trueque, turno_dia, intercambio.trueque_1.usuario.filial)
            send_mail_usuario_producto(intercambio.producto_2.usuario.mail,codigo_usuario_producto, turno_dia, intercambio.trueque_1.usuario.filial)
            #guarda los codigos que les mando, para q dps un ayudante verifique a la hora de hacer el verificar codigo
            intercambio.save()
            
            #notifica a los 2 participantes de un trueque aceptado que se realizo el mismo
            #tambien manda notificacion a los otros usuarios que ofertaron algun producto, informando que eligio otra oferta
            notificar_trueque_aceptado(intercambio)
            return render(request, 'trueques_en_espera_de_confirmacion.html', {'intercambios': intercambios,  'error': error_message})

        #el dueño del trueque rechaza el producto ofertado
        elif action == 'rechazar':
            intercambio.estado = 'Rechazado'
            intercambio.save()
            mensaje_rechazo = f"Tu oferta para el trueque '{intercambio.trueque_1.titulo}' fue rechazada. Motivo: {motivo_rechazo}"
            notificacion_rechazo = Notificacion(usuario=intercambio.producto_2.usuario, mensaje=mensaje_rechazo)
            notificacion_rechazo.save()
            return render(request, 'trueques_en_espera_de_confirmacion.html', {'intercambios': intercambios,  'error': error_message})

    return render(request, 'trueques_en_espera_de_confirmacion.html', {'intercambios': intercambios,  'error': error_message})

@login_required
def ver_perfil_usuario(request):
    return render(request, 'ver_perfil_usuario.html')

def buscar_proximo_turno_disponible(filial):
    hoy = date.today()
    proximo_sabado = hoy + timedelta((5-hoy.weekday()) % 7)
    proximo_domingo = hoy + timedelta((6-hoy.weekday()) % 7)

    for i in range(4):  # buscar en las próximas 4 semanas
        if Turno.objects.filter(dia=proximo_sabado, filial=filial).count() < 50:
            return proximo_sabado
        if Turno.objects.filter(dia=proximo_domingo, filial=filial).count() < 50:
            return proximo_domingo
        proximo_sabado += timedelta(days=7)
        proximo_domingo += timedelta(days=7)
    return None