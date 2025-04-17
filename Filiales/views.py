from django.shortcuts import render, redirect, get_object_or_404
from .forms import FilialForm
from .models import Filial
from django.contrib.auth.decorators import login_required, user_passes_test
from administrador.views import user_authenticated, user_is_specific_user
from django.urls import reverse
from Trueques.models import Trueque
from accounts.models import Usuario

@login_required
@user_passes_test(user_authenticated)
def create_filial(request):
    if request.method == 'POST':
        form = FilialForm(request.POST)
        if form.is_valid():
            direccion = form.cleaned_data['direccion']
            nombre = form.cleaned_data['nombre']
            if Filial.objects.filter(nombre=nombre).exists():
                form.add_error('direccion', 'El nombre ya existe.')
            elif Filial.objects.filter(direccion=direccion).exists():
                form.add_error('direccion', 'La filial ya existe.')
            else:
                Filial.objects.create(direccion=direccion, nombre=nombre)
                return redirect(reverse('Filiales:list_filiales'))
    else:
        form = FilialForm()
    return render(request, 'create_filial.html', {'form': form})


def list_filiales(request):
    filiales = Filial.objects.filter(borrado=False)
    if (request.method == "POST"):
        filial_id = request.POST.get('filial_id')
        filial = Filial.objects.get(id=filial_id)
        filial.borrado = True
        filial.save()

        ayudante_relacionado = filial.ayudante
        if ayudante_relacionado:
            ayudante_relacionado.borrado = True
            ayudante_relacionado.save()

    return render(request, 'list_filiales.html', {'filiales': filiales})

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def modify_filial(request):
    filial_id = request.session.get('filial_id')
    filial = get_object_or_404(Filial, id=filial_id)
    if request.method == 'POST':
        form = FilialForm(request.POST, instance=filial)
        if form.is_valid():
            direccion = form.cleaned_data['direccion']
            if Filial.objects.exclude(id=filial_id).filter(direccion=direccion).exists():
                form.add_error('direccion', 'La filial ya existe.')
            else:
                form.save()
                return redirect(reverse('Filiales:list_filiales'))
    else:
        form = FilialForm(instance=filial)
    return render(request, 'modify_filial.html', {'form': form})

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def set_filial_id(request, filial_id):
    request.session['filial_id'] = filial_id
    # Redirigir a la vista correspondiente
    next_url = request.GET.get('next', 'Filiales:list_filiales')
    return redirect(next_url)

@login_required
@user_passes_test(user_authenticated)
def ver_datos_filiales(request):
    print("entro")
    filial_id = request.session.get('filial_id')
    print(filial_id)
    try:
        filial = Filial.objects.get(id=filial_id)
    except Filial.DoesNotExist:
        return redirect('Filiales:select_filial')

    print(f"Filial: {filial}")
    
    usuarios = Usuario.objects.filter(filial=filial)
    print(f"Usuarios: {usuarios}")

    trueques = Trueque.objects.filter(usuario__in=usuarios)
    print(f"Trueques: {trueques}")

    accepted_trueques = trueques.filter(estado_trueque='Aceptado')
    canceled_trueques = trueques.filter(estado_trueque='Cancelado')
    pending_trueques = trueques.filter(estado_trueque='Pendiente')

    no_data = not trueques.exists()

    return render(request, 'ver_datos_filiales.html', {
        'filial': filial,
        'accepted_trueques': accepted_trueques,
        'canceled_trueques': canceled_trueques,
        'pending_trueques': pending_trueques,
        'no_data': no_data,
    })

@login_required
@user_passes_test(user_authenticated)
def select_filial(request):
    filiales = Filial.objects.filter(borrado = False)
    if request.method == 'POST':
        filial_id = request.POST.get('filial_id')
        if filial_id:
            request.session['filial_id'] = filial_id
            return redirect('Filiales:ver_datos_filiales')
    return render(request, 'seleccionar_filial.html', {'filiales': filiales})
