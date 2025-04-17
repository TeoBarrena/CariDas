from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from Productos.models import Producto
from Trueques.models import Trueque
from .forms import RegistroAyudanteForm
from Reseñas.models import Review
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
import re
import os
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.models import User
from Filiales.models import Filial
from Pantalla_principal.models import Notificacion
# Create your views here

def user_authenticated(user):
    return user.is_authenticated

def error404(request, exception=None):
    return render(request, 'error404.html', status=404)


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
def seleccionar(request):
    return render(request, 'select.html')


@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def show_usuarios(request):
    usuarios = Usuario.objects.all()
    if request.method == 'GET':
      return render(request, 'show_usuarios.html', {'usuarios': usuarios})
    elif request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        user = get_object_or_404(Usuario, id=user_id)

        if action == 'block':
            user.blocked = True
            user.save()
            return render(request, 'show_usuarios.html', {'usuarios': usuarios})

        elif action == 'view_profile':
            request.session['view_user_id'] = user_id
            return redirect('ver_perfil',request.session['view_user_id'])
        elif action == 'edit_profile':
            request.session['view_user_id'] = user_id
            return redirect('editar_perfil_admin')


    # If the action is not recognized, you may return a bad request response or handle it appropriately
    return render(request, 'show_usuarios.html', {'usuarios': usuarios})
  
@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def show_productos  (request):
  productos = Producto.objects.filter(borrado=False)
  print(productos)
  if request.method == 'GET' :
      return render(request, 'show_productos.html', {'productos': productos})
  elif request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        prod = Producto.objects.get(id=producto_id)
        mensaje_rechazo = f"Tu producto '{prod.titulo}' ha sido eliminado por el administrador. Motivo: incumplia las normas"
        notificacion_rechazo = Notificacion(usuario=prod.usuario, mensaje=mensaje_rechazo)
        notificacion_rechazo.save()
        prod.delete()
        return render(request, 'show_productos.html', {'productos': productos})


@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def show_donaciones  (request):
    return render(request, 'show_donaciones.html')

def send_email(mail, trueque):
    context = {'trueque': trueque}
    template = get_template('trueuqe_eliminado.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Trueque Eliminado',  # Asunto del correo
        'Su trueque ha sido eliminado.',  # Cuerpo del correo en texto plano
        settings.EMAIL_HOST_USER,  # Desde que cuenta se manda
        [mail],  # A quién se envía el correo
    )
    email.attach_alternative(content, 'text/html')
    email.send()

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def show_trueques  (request):
    trueques = Trueque.objects.all()
    if request.method == 'GET' :
        return render(request, 'show_trueques.html', {'trueques': trueques})
    elif request.method == 'POST':
            producto_id = request.POST.get('producto_id')
            producto_id = request.POST.get('producto_id')
            trueque = Trueque.objects.get(id=producto_id)
            user_email = trueque.usuario.mail 
            # Envía un correo electrónico al usuario
            send_email(user_email, trueque)

            # Elimina el trueque
            trueque.estado_trueque = 'Eliminado'
            trueque.save()
            return render(request, 'show_trueques.html', {'trueques': trueques})

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def registrar_ayudante(request):
    if request.method == 'POST':
        form = RegistroAyudanteForm(request.POST, request.FILES)
        if form.is_valid():
            filial = form.cleaned_data['filial']
            if verificar_dni_unico(form.cleaned_data['dni']):
                return render(request, 'registration/registrar_usuario.html', {'form': form, 'error_dni':True})
            if verificar_mail_unico(form.cleaned_data['email']):
                return render(request, 'registration/registrar_usuario.html', {'form': form,'error_mail':True})
            if not (verificar_prefijo_celular(form.cleaned_data['numero'])):
                return render(request, 'registration/registrar_usuario.html', {'form': form,'error_prefijo':True})
            if not(verificar_cant_numeros_celular(form.cleaned_data['numero'])):
                return render(request, 'registration/registrar_usuario.html', {'form': form,'error_cant_numeros':True})
            if form.cleaned_data['edad'] < 18:
                return render(request, 'registration/registrar_usuario.html', {'form': form,'error_edad':True})
            else:
                ayudante = Usuario(
                    dni = form.cleaned_data['dni'],
                    first_name = form.cleaned_data['name'],
                    last_name = form.cleaned_data['apellido'],
                    age = form.cleaned_data['edad'],
                    mail = form.cleaned_data['email'],
                    num = form.cleaned_data['numero'],
                    profile_picture = form.cleaned_data['foto_perfil'],
                    filial = filial,
                    is_ayudante = True,
                )
                # Hashear la contraseña y luego guardar el ayudante en la base de datos
                if (verificar_contraseña(form.cleaned_data['contrasena1'])):
                    if (verificar_contraseñas_iguales(form.cleaned_data['contrasena1'],form.cleaned_data['contrasena2'])):
                        ayudante.password = make_password(form.cleaned_data['contrasena1'])
                        ayudante.save()
                        filial.ayudante = ayudante
                        filial.save()
                        return redirect('vista_admin') 
                    else:
                        return render(request, 'registrar_ayudante.html', {'form': form,'error_contraseñas':True})
                else:
                    return render(request, 'registrar_ayudante.html', {'form': form,'error_estructura_contrasena':True})
 # Redirige a la página de login o a donde prefieras
    else:
        form = RegistroAyudanteForm()
        cantfiliales = Filial.objects.filter(borrado=False, ayudante_id=None).count()
        if (cantfiliales == 0):
            return render(request, 'registrar_ayudante.html', {'form': form,'error_cantidad_filiales':True})
    return render(request, 'registrar_ayudante.html', {'form': form})

def verificar_contraseña(contraseña):
    # La expresión regular ^(?=.*\d)(?=.*[a-zA-Z]).{6,}$ verifica:
    # - (?=.*\d): Al menos un dígito.
    # - (?=.*[a-zA-Z]): Al menos una letra.
    # - .{6,}: Al menos 6 caracteres.
    patron = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,}$')
    if patron.match(contraseña):
        return True
    else:
        return False

def verificar_dni_unico(dni):
    #retorna True si existe en la base de datos, es decir si ya esta cargado un usuario con ese DNI
    return Usuario.objects.filter(dni = dni).exists()

def verificar_mail_unico(mail):
    #retorna True si existe un usuario con ese mail en la base de datos
    return Usuario.objects.filter(mail = mail).exists()

def verificar_contraseñas_iguales(password1,password2):
    return password1 == password2

def verificar_prefijo_celular(numero):
    #retorna True si empieza con 221 el celular
    numero = str(numero)
    return numero.startswith("221")

def verificar_cant_numeros_celular(numero):
    #retorna True si tiene 10 numeros el celular
    numero = str(numero)
    return len(numero) == 10

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def vista_admin(request):
    return render(request, 'vista_admin.html')


@login_required
@user_passes_test(user_authenticated)
def ver_perfil(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)
    if not user_id:
        return HttpResponseForbidden("No user ID found in session")

    user = get_object_or_404(Usuario, id=user_id)
    trueques = Trueque.objects.filter(usuario_id=user_id,estado_trueque='Completado')
    productos = Producto.objects.filter(usuario_id=user_id)
    star_range = range(1, 6)  # Lista de 1 a 5 para las estrellas
    reviews = Review.objects.filter(user_reseniado__id=user_id)


    return render(request, 'ver_perfil.html', {
        'usuario': user,
        'trueques': trueques,
        'productos': productos,
        'reviews': reviews,
        'star_range': star_range
    })

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def editar_perfil(request):
    user_id = request.session.get('view_user_id')
    usuario = get_object_or_404(Usuario, id=user_id)
    filiales_permitidas = Filial.objects.filter(borrado=False)  # Obtener filiales permitidas
    
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        new_value = request.POST.get('new_value')
        new_file = request.FILES.get('profile_picture', None)

        if field_name and (new_value or new_file):
            if field_name == 'mail' and Usuario.objects.exclude(id=usuario.id).filter(mail=new_value).exists():
                return JsonResponse({'success': False, 'error': 'El correo ya está en uso.'})
            if field_name == 'num' and not verificar_prefijo_celular(new_value):
                return JsonResponse({'success': False, 'error': 'El prefijo del número es incorrecto.'})
            if field_name == 'num' and not verificar_cant_numeros_celular(new_value):
                return JsonResponse({'success': False, 'error': 'La cantidad de números es incorrecta.'})
            if field_name == 'dni' and verificar_dni_unico(new_value):
                return JsonResponse({'success': False, 'error': 'El DNI ya se encuentra registrado.'})
            if field_name == 'age':
                edad = int(new_value)
                if edad < 18:
                    return JsonResponse({'success': False, 'error': 'El usuario es menor de edad.'})
            if field_name == 'profile_picture' and new_file:
                filename = os.path.basename(new_file.name)
                relative_path = os.path.join('media', filename)
                full_path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(full_path, 'wb+') as destination:
                    for chunk in new_file.chunks():
                        destination.write(chunk)
                
                usuario.profile_picture.name = relative_path
                usuario.save()

                return JsonResponse({'success': True, 'new_value': full_path})
            elif field_name == 'filial':
                filial = Filial.objects.filter(borrado=False).get(id=new_value)
                usuario.filial = filial
                usuario.save()
                return JsonResponse({'success': True, 'new_value': filial.direccion})
            else:
                setattr(usuario, field_name, new_value)
                usuario.save()
                return JsonResponse({'success': True, 'new_value': new_value})

        return JsonResponse({'success': False, 'error': 'Campo no válido.'})
    
    return render(request, 'editar_perfil_admin.html', {'user': usuario, 'filiales': filiales_permitidas})
