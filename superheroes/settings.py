import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Missing Django SECRET_KEY in the environmental variables.')

SUPERHEROAPI_TOKEN = os.getenv('SUPERHEROAPI_TOKEN')
if not SUPERHEROAPI_TOKEN:
    raise ImproperlyConfigured('Missing Django SUPERHEROAPI_TOKEN in the environmental variables.')

DEBUG = (os.getenv('DEBUG') or 'False').lower() in ['true', '1', 't', 'yes']

ALLOWED_HOSTS = (os.getenv('DJANGO_ALLOWED_HOSTS') or '127.0.0.1').split(',')
CSRF_TRUSTED_ORIGINS = (os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS') or 'http://127.0.0.1,https://127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'superheroes_api.apps.SuperheroesApiConfig',
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

ROOT_URLCONF = 'superheroes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'superheroes.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{os.getenv("DATABASE_ENGINE") or "sqlite3"}',
        'NAME': os.getenv('DATABASE_NAME') or BASE_DIR / 'db.sqlite3',
        'USER': os.getenv('DATABASE_USERNAME') or 'dbuser',
        'PASSWORD': os.getenv('DATABASE_PASSWORD') or 'dbpassword',
        'HOST': os.getenv('DATABASE_HOST') or 'db',
        'PORT': os.getenv('DATABASE_PORT') or '5432',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
