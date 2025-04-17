from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CategoriaForm, ProductForm
from .models import Categoria, Producto
from django.urls import reverse
from spanlp.palabrota import Palabrota
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponse
import os
from django.conf import settings
from Trueques.models import Trueque, IntercambioTrueque

import os
from django.conf import settings
from Trueques.models import Trueque
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from Pantalla_principal.models import Notificacion
from django.db.models import Q


def user_authenticated(user):
    return user.is_authenticated

def user_is_specific_user(user_id):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.id == user_id:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def create_category(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            puntos = form.cleaned_data['puntos']
            # Verificar si la categoría ya existe
            if Categoria.objects.filter(nombre=nombre).exists():
                form.add_error('nombre', 'La categoría ya existe.')
            else:
                Categoria.objects.create(nombre=nombre, puntos = puntos)
                return redirect(reverse('Productos:list_category'))
    else:
        form = CategoriaForm()
    return render(request, 'create_category.html',{'form':form})

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        palabrota = Palabrota()
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            categoria_id = form.cleaned_data['categoria']
            categoria = Categoria.objects.get(id=categoria_id)
            usuario = request.user
            productos_del_usuario = usuario.productos.filter(borrado=False)

            if productos_del_usuario.filter(titulo=titulo).exists():
                form.add_error('titulo', 'Ya tenes un producto cargado con ese titulo!.')
            elif palabrota.contains_palabrota(descripcion):
                form.add_error('descripcion', 'la descripcion contiene contenido vulgar!')
            else:
                foto_producto = form.cleaned_data['foto_producto']
                if not foto_producto:
                    form.add_error('foto_producto', 'La foto del producto es obligatoria.')
                else:
                    filename = os.path.basename(foto_producto.name)
                    relative_path = os.path.join('media', filename)
                    full_path = os.path.join(settings.MEDIA_ROOT, filename)
                    
                    # Guardar el archivo en la ruta especificada
                    with open(full_path, 'wb+') as destination:
                        for chunk in foto_producto.chunks():
                            destination.write(chunk)
                    

                    producto = Producto.objects.create(
                        titulo=titulo, 
                        descripcion = descripcion,
                        estado = form.cleaned_data['estado'],
                        foto_producto = filename,
                        categoria = categoria,
                        usuario = usuario,
                        )
                    producto.save()

                    return redirect(reverse('Usuario:show_productos_usuario'))
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'create_product.html',{'form':form})



@login_required
def delete_category(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        if categoria_id:
            try:
                categoria = get_object_or_404(Categoria, id=categoria_id)
                categoria.borrado = True
                categoria.save()

                # Marcar como borrados los productos relacionados
                productos_relacionados = Producto.objects.filter(categoria=categoria)
                for producto in productos_relacionados:
                    if (producto.borrado == False):
                        user_email = producto.usuario.mail
                        send_email(user_email, producto)
                        producto.borrado = True
                        producto.save()
                    
                    trueques_relacionados = Trueque.objects.filter(producto=producto)
                    for trueque in trueques_relacionados:
                        trueque.estado_trueque = 'Eliminado'
                        trueque.save()

                return redirect(reverse('Productos:list_category'))
            except Exception as e:
                print(f"Error deleting category: {e}")  # Debugging line
                return HttpResponse(f"Error: {e}")
        else:
            return HttpResponse("Error: No se recibió el ID de la categoría.")
    return HttpResponse("Método no permitido.", status=405)

@login_required
def list_category(request):
    categorias = Categoria.objects.filter(borrado=False)
    return render(request, 'list_category.html', {'categorias': categorias})

@login_required
def send_email(mail, producto):
    context = {'producto': producto}
    template = get_template('producto_eliminado.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Producto Eliminado',  # Asunto del correo
        'Su producto ha sido eliminado.',  # Cuerpo del correo en texto plano
        settings.EMAIL_HOST_USER,  # Desde qué cuenta se manda
        [mail],  # A quién se envía el correo
    )
    email.attach_alternative(content, 'text/html')
    email.send()