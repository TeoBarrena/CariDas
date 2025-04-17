from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoticiaForm
from .models import Noticia
from django.contrib.auth.decorators import login_required, user_passes_test
from administrador.views import user_authenticated, user_is_specific_user



@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def agregar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Pantalla_principal:Pantalla_principal')
    else:
        form = NoticiaForm()
    return render(request, 'agregar_noticia.html', {'form': form})

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def delete_noticia(request):
    if request.method == 'POST':
        noticia_id = request.POST.get('noticia_id')
        if noticia_id:
            categoria = get_object_or_404(Noticia, id=noticia_id)
            categoria.borrado = True
            categoria.save()

    return redirect('Pantalla_principal:Pantalla_principal')





from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
from .forms import NoticiaForm

def set_noticia_id(request):
    if request.method == 'POST':
        noticia_id = request.POST.get('noticia_id')
        request.session['noticia_id'] = noticia_id
        return redirect('Noticias:modify_noticia')

def modify_noticia(request):
    noticia_id = request.session.get('noticia_id')
    if noticia_id is None:
        return redirect('Pantalla_principal:Pantalla_principal')
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('Pantalla_principal:Pantalla_principal')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'modify_noticia.html', {'form': form, 'noticia_id': noticia_id})
