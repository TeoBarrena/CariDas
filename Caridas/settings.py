"""
Django settings for Caridas project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#lo agregue yo esto de media
MEDIA_URL = '/media/' #esto es para que las fotos vayan a esta carpeta
MEDIA_ROOT = os.path.join(BASE_DIR, 'accounts','static','media') #esto es para que las fotos vayan a esta carpeta

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tui!!_om=by3$3((au1+hsv8gjma!u-1@rb-e$6azr!xfrv*y4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Productos',
    'Filiales',
    'accounts',
    'Ayudante',
    'Pantalla_principal',
    'administrador',
    'Caridas',
    'Usuario',
    'Intercambiar_puntos',
    'Trueques',
    'busqueda',
    'Noticias',
    'Reseñas',
    'Donaciones',
    'Estadisticas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Caridas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Caridas', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Caridas.context_processors.notificaciones_no_leidas',
            ],
        },
    },
]

WSGI_APPLICATION = 'Caridas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Ruta absoluta donde se recopilan los archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Productos/static'),
    os.path.join(BASE_DIR, 'Filiales/static'),
    os.path.join(BASE_DIR, 'accounts/static'),
    os.path.join(BASE_DIR, 'Caridas/static'),
    os.path.join(BASE_DIR, 'Pantalla_principal/static'),
    os.path.join(BASE_DIR, 'administrador/static'),
    os.path.join(BASE_DIR, 'Usuario/static'),
    os.path.join(BASE_DIR, 'busqueda/static'),
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.Usuario'

EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pixelsolution48@gmail.com'
EMAIL_HOST_PASSWORD = 'i u r t m w d p m s m k x h k t'
EMAIL_USE_TLS = True

LOGIN_URL = '/accounts/login/'

MERCADOPAGO_PUBLIC_KEY = 'TEST-313f2a16-a406-477c-a160-0946cc4426f5'
MERCADOPAGO_ACCESS_TOKEN = 'TEST-6677789934586725-061823-8317bffc7c2fd076b6ab01906bdf8ec1-230382078'