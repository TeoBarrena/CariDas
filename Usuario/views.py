from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Productos.models import Producto
from django.db.models import Q
from Trueques.models import Trueque,IntercambioTrueque
from Productos.models import Producto
from django.db.models import Q
from Trueques.models import Trueque,IntercambioTrueque
from Reseñas.models import Review
from Trueques.models import Trueque
from Pantalla_principal.models import Notificacion
@login_required
def opciones_trueque(request):
    return render(request, 'selectUsuario.html') 

@login_required
def show_productos(request):
    productos = Producto.objects.filter(usuario=request.user, borrado=False)
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        try:
            product = Producto.objects.get(id=producto_id, usuario=request.user)
            product.borrado = True
            product.save()

            trueques_relacionados = Trueque.objects.filter(producto=product)
            for trueque in trueques_relacionados:
                trueque.estado_trueque = 'Eliminado'
                trueque.save()
                
                # Crear notificación para el usuario del trueque
                mensaje_trueque = f"Tu trueque '{trueque.titulo}' ha sido eliminado."
                notificacion_trueque = Notificacion(usuario=trueque.usuario, mensaje=mensaje_trueque)
                notificacion_trueque.save()

                # Notifica en el caso de que el dueño del truque ofertó y luego lo eliminó
                intercambios = IntercambioTrueque.objects.filter(Q(trueque_1=trueque))
                for intercambio in intercambios:
                    intercambio.estado = 'Eliminado'
                    intercambio.save()

                    if intercambio.producto_2.usuario != trueque.usuario:
                        mensaje_producto = f"Tu solicitud para el trueque '{trueque.titulo}' ha sido eliminada porque el producto fue eliminado."
                        notificacion_producto = Notificacion(usuario=intercambio.producto_2.usuario, mensaje=mensaje_producto)
                        notificacion_producto.save()


            # Notifica en el caso de que un usuario hay ofertedo y luego elimando el producto
            intercambios = IntercambioTrueque.objects.filter(Q(producto_2__id=product.id), estado = "Espera de confirmacion")
            for intercambio in intercambios:
                intercambio.estado = 'Eliminado'
                intercambio.save()

                mensaje_producto = f"Tu solicitud para el trueque '{intercambio.trueque_1.titulo}' ha sido eliminada porque el producto fue eliminado."
                notificacion_producto = Notificacion(usuario=intercambio.producto_2.usuario, mensaje=mensaje_producto)
                notificacion_producto.save()

                mensaje_trueque_usuario = f"Una solicitud de intercambio relacionada a tu trueque '{intercambio.trueque_1.titulo}' ha sido eliminado."
                notificacion_trueque_usuario = Notificacion(usuario=intercambio.trueque_1.usuario, mensaje=mensaje_trueque_usuario)
                notificacion_trueque_usuario.save()

        except Producto.DoesNotExist:
            return render(request, 'show_productos_usuario.html', {'productos': productos, 'error_message': 'Producto eliminado'})
    
    return render(request, 'show_productos_usuario.html', {'productos': productos})

@login_required
def show_trueques  (request):
    user_id = request.user.id
    #trueques = Trueque.objects.filter(usuario_id=request.user.id).exclude(estado_trueque='Eliminado')
    trueques_aceptados = IntercambioTrueque.objects.filter(
    Q(trueque_1__usuario_id=request.user.id) | Q(producto_2__usuario_id=request.user.id),
    estado='Aceptado'
    )
    #trueques_cancelados = IntercambioTrueque.objects.filter(Q(trueque_1__usuario_id=request.user.id) | Q(producto_2__usuario_id=request.user.id), estado='Rechazado')
    trueques_cancelados_creador = IntercambioTrueque.objects.filter(
        trueque_1__usuario_id=request.user.id, estado='Rechazado'
    )
    trueques_cancelados_ofertante = IntercambioTrueque.objects.filter(
        producto_2__usuario_id=request.user.id, estado='Rechazado'
    )
    trueques_pendientes = Trueque.objects.filter(usuario_id = request.user.id, estado_trueque='Pendiente')
    trueques_espera_de_confirmacion = IntercambioTrueque.objects.filter(trueque_1__usuario_id=request.user.id, estado='Espera de confirmacion').count()
    trueques_completados = IntercambioTrueque.objects.filter(
    Q(trueque_1__usuario_id=request.user.id) | Q(producto_2__usuario_id=request.user.id),
    estado='Completado'
    )

    # Obtener las reseñas realizadas
    reseñas_realizadas = Review.objects.filter(user_id=user_id).values_list('trade_id', flat=True)
    #aca esta la eliminacion del trueque
    if request.method == 'POST':
        trueque_id = request.POST.get('trueque_id')
        #asad
        try:
            trueque = Trueque.objects.get(id=trueque_id, usuario=request.user)
            trueque.estado_trueque = 'Eliminado' 
            trueque.save()

            # Crear notificación para el usuario del trueque
            mensaje_trueque = f"Tu trueque '{trueque.titulo}' ha sido eliminado."
            notificacion_trueque = Notificacion(usuario=trueque.usuario, mensaje=mensaje_trueque)
            notificacion_trueque.save()

            # Crear notificación para el usuario del producto si es diferente
            intercambios = IntercambioTrueque.objects.filter(producto_2__id=trueque.producto.id, producto_2__borrado= False)
            for intercambio in intercambios:
                if intercambio.producto_2.usuario != trueque.usuario:
                    mensaje_producto = f"El trueque al que solicitaste con tu producto '{intercambio.producto_2.titulo}' ha sido eliminado."
                    notificacion_producto = Notificacion(usuario=intercambio.producto_2.usuario, mensaje=mensaje_producto)
                    notificacion_producto.save()


        except Trueque.DoesNotExist:
            return render(request, 'show_trueques_usuario.html', {'error_message': 'Trueque eliminado','trueques_aceptados':trueques_aceptados.count()})
    
    context = {
        'trueques_aceptados': trueques_aceptados,
        'trueques_cancelados_creador': trueques_cancelados_creador,
        'trueques_cancelados_ofertante': trueques_cancelados_ofertante,
        'trueques_pendientes': trueques_pendientes,
        'trueques_en_espera_de_confirmacion': trueques_espera_de_confirmacion,
        'trueques_completados':trueques_completados,
        'reseñas_realizadas': reseñas_realizadas
    }
    return render(request, 'show_trueques_usuario.html', context)
