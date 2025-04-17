from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistroUsuarioForm, LoginForm
from .models import Usuario
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from django.contrib.auth import login,logout
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random,re, os
from Filiales.models import Filial
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

def signin(request):
    if request.method == 'GET':
        form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if verificar_user_bloqueado(user): 
                messages.error(request, 'El usuario se encuentra bloqueado')
            else:
                next_url = request.GET.get('next')
                if (user.id == 1):
                    login(request, user)
                    if next_url:
                        return redirect(next_url)
                    return redirect('vista_admin')
                elif (user.is_ayudante):
                    request.session['user_id'] = user.id
                    request.session['mail'] = user.mail 
                    codigo_generado = random.randint(100000,999999)
                    request.session['codigo_generado'] =  codigo_generado#lo pongo aca para que no se actualice en enviar codigo
                    return redirect("Ayudante:enviar_codigo") 
                else:
                    login(request, user)
                    if next_url:
                        return redirect(next_url)
                    return redirect('Pantalla_principal:Pantalla_principal')
        else:
            messages.error(request, 'DNI o contraseña incorrectos')  # Agrega un mensaje de error
    return render(request, 'registration/login.html', {'form': form})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        # Modificar el widget del campo de nombre de usuario para establecer la clase y el placeholder
        self.fields['username'].widget.attrs.update({'class': 'username', 'placeholder': 'Ingrese su DNI'})
        # Modificar el widget del campo de contraseña para establecer la clase y el placeholder
        self.fields['password'].widget.attrs.update({'class': 'password', 'placeholder': 'Ingrese su contraseña'})
        
    def clean(self):
        dni = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if dni and password:
            self.cleaned_data['username'] = dni
            self.user_cache = authenticate(self.request, username=dni, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    'DNI o contraseña incorrectos',  # Cambia el mensaje de error aquí
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
    
def verificar_user_bloqueado(user):
    if user.blocked:
        return True
    return False

def cerrar_sesion(request):
    logout(request)
    return redirect('accounts:login')


#anda bien
def send_email(mail,numero):

    context = {'numero':numero, 'mostrar_codigo':True}
    
    template = get_template('registration/correo.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Cambio de contraseña', #titulo que le aparece en el mail
        'no se que sentido tiene esto, pero va',
        settings.EMAIL_HOST_USER, #desde que cuenta se manda
        [mail], #esto es a quien se lo mande
    )
    email.attach_alternative(content, 'text/html')
    email.send()


#anda bien
def reestablecer_contrasena(request):
    if request.method == 'POST':
        numero = random.randint(100000, 999999)
        mail = request.POST.get('mail')
        if Usuario.objects.filter(mail = mail).exists(): #verifica que el mail ingresado se encuentre en la BD, asi no le manda a uno que no existe
            send_email(mail,numero)
            request.session['mail'] = mail #para establecer un valor corchete, para obtener va parentesis
            request.session['numero'] = numero
            return redirect('accounts:verificar_codigo')#,numero=numero, mail=mail)
        else:
            return render(request, 'registration/reestablecer_contrasena.html',{'error':True})        
    return render(request, 'registration/reestablecer_contrasena.html',{'error':False})

#anda bien
def verificar_codigo(request):#,numero,mail):
    mail = request.session.get('mail')
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        if codigo_ingresado == str(request.session.get('numero')):
            return redirect('accounts:cambiar_contraseña')#,mail)
        else:
            return render(request, 'registration/verificar_codigo.html', {'mail':mail,'error': True})
    return render(request, 'registration/verificar_codigo.html', {'mail': mail})

#anda bien
def cambiar_contrasena(request):#,mail): #el mail es para aplicar el dps en la base de datos y cambiar la contraseña
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not(verificar_contraseñas_iguales(password1,password2)):
            return render(request,'registration/cambiar_contrasena.html', {'error_passwords_distintas':True, 'error_password_invalida':False})
        if not (verificar_contraseña(password1)):
            return render(request,'registration/cambiar_contrasena.html', {'error_passwords_distintas':False,'error_password_invalida':True})
        mail = request.session.get('mail')
        user = Usuario.objects.get(mail = mail) #el filter devuelve un QuerySet, con get obtenes una instancia de Usuario
        user.set_password(password1)  
        user.save()
        messages.success(request, 'Contraseña cambiada exitosamente. Por favor inicia sesión con tu nueva contraseña.')
        return redirect('accounts:login')
    return render(request,'registration/cambiar_contrasena.html')

#anda bien
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

#anda bien listo
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            #verificar que el numero empiece con 221 
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
                user = Usuario(
                    dni = form.cleaned_data['dni'],  # Cambia 'username' por 'dni'
                    first_name = form.cleaned_data['name'],
                    last_name = form.cleaned_data['apellido'],
                    age = form.cleaned_data['edad'],
                    mail = form.cleaned_data['email'],
                    num = form.cleaned_data['numero'],
                    filial = form.cleaned_data['filial']
                )
                foto_perfil = form.cleaned_data['foto_perfil']
                if foto_perfil:
                    filename = os.path.basename(foto_perfil.name)
                    relative_path = os.path.join('media', filename)
                    full_path = os.path.join(settings.MEDIA_ROOT, filename)
                    
                    # Guardar el archivo en la ruta especificada
                    with open(full_path, 'wb+') as destination:
                        for chunk in foto_perfil.chunks():
                            destination.write(chunk)
                    
                    user.profile_picture.name = relative_path
                
                # Hashear la contraseña y luego guardar el usuario en la base de datos
                #primero tiene que hacer verificacion de la estructura de la contraseña y despues preguntar si son iguales
                if (verificar_contraseña(form.cleaned_data['contrasena1'])):
                    if (verificar_contraseñas_iguales(form.cleaned_data['contrasena1'],form.cleaned_data['contrasena2'])):
                        user.set_password(form.cleaned_data['contrasena1'])  
                        user.save()
                        return redirect('accounts:login')
                    else:
                        return render(request, 'registration/registrar_usuario.html', {'form': form,'error_contraseñas':True})
                else:
                    return render(request, 'registration/registrar_usuario.html', {'form': form,'error_estructura_contrasena':True})
    else:
        form = RegistroUsuarioForm()
        cantfiliales = Filial.objects.filter(borrado=False).count()
        if (cantfiliales == 0):
            return render(request, 'registration/registrar_usuario.html', {'form': form,'error_cantidad_filiales':True})

    return render(request, 'registration/registrar_usuario.html', {'form': form})

@login_required
def editar_perfil(request):
    usuario = request.user
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

            if field_name == 'profile_picture' and new_file:
                filename = os.path.basename(new_file.name)
                relative_path = os.path.join('media', filename)
                full_path = os.path.join(settings.MEDIA_ROOT, filename)
                # Guarda el archivo en la ruta especificada
                with open(full_path, 'wb+') as destination:
                    for chunk in new_file.chunks():
                        destination.write(chunk)
                
                # Actualiza el campo del modelo con la ruta relativa
                usuario.profile_picture.name = relative_path
                usuario.save()

                return JsonResponse({'success': True, 'new_value': full_path})
            else:
                setattr(usuario, field_name, new_value)
                usuario.save()
                return JsonResponse({'success': True, 'new_value': new_value})

        return JsonResponse({'success': False, 'error': 'Campo no válido. '})
    
    return render(request, 'registration/editar_perfil.html', {'user': usuario})
