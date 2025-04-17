from Pantalla_principal.models import Notificacion

def notificaciones_no_leidas(request):
    if request.user.is_authenticated:
        return {
            'notificaciones_no_leidas': Notificacion.objects.filter(usuario=request.user, leida=False).count()
        }
    return {}