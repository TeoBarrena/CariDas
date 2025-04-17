from django.shortcuts import render
from Productos.models import Categoria
from Trueques.models import Trueque
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def listar_trueques(request):
    estado = request.GET.get('estado')
    categoria_id = request.GET.get('categoria')
    query = request.GET.get('q')
    user = request.user


    trueques = Trueque.objects.select_related('producto', 'producto__categoria').filter(~Q(producto__usuario=user), estado_trueque='Pendiente')


    if estado:
        trueques = trueques.filter(estado=estado)

    if categoria_id:
        trueques = trueques.filter(producto__categoria_id=categoria_id) 

    if query:
        trueques = trueques.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))

    categorias = Categoria.objects.filter(borrado=False)


    context = {
        'trueques': trueques,
        'estado': estado,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'query': query,
    }

    return render(request, 'listar_Trueques.html', context)


