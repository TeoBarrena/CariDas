from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Noticias.models import Noticia
from .models import Notificacion
from Noticias.models import Noticia

def pantalla_principal(request):
    noticias = Noticia.objects.filter(borrado = False).order_by('-fecha_creado')
    return render(request, 'indexPantalla_principal.html', {'noticias': noticias})

@login_required
def listar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user, borrado = False).order_by('-fecha_creacion')
    # Marcar las notificaciones como leídas
    notificaciones.update(leida=True)
    context = {
        'notificaciones': notificaciones
    }
    return render(request, 'listar_notificaciones.html', context)

@login_required
def donaciones(request):
    return render(request, 'indexDonaciones.html')

@login_required
def delete_notificacion(request):
    print("inside")
    if request.method == 'POST':
        notificacion_id = request.POST.get('notificacion_id')
        print(notificacion_id)
        if notificacion_id:
            notificacion = get_object_or_404(Notificacion, id=notificacion_id)
            notificacion.borrado = True
            notificacion.save()

    return redirect('Pantalla_principal:listar_notificaciones')