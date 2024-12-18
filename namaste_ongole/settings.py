"""
Django settings for namaste_ongole project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""


# import django_heroku
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import environ
import dj_database_url


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env('DEBUG')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ka2lurddl**i0v7sulf&8@0dgg1i)+flzh2by%!$q+!6x*p834'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IMPORT_EXPORT_USE_TRANSACTIONS = False
#ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

# FCM_DJANGO_SETTINGS = {
#         "FCM_SERVER_KEY": env("FCM_SERVER_KEY")
# }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_user_agents',
    'rest_framework',
    'rest_framework.authtoken',
    'branch',
    'menu',
    'user',
    'order',
    'rest_framework_swagger',
    'import_export',
    'fcm_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'namaste_ongole.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Cache backend is optional, but recommended to speed up user agent parsing
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

WSGI_APPLICATION = 'namaste_ongole.wsgi.application'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

MIDDLEWARE_CLASSES = (
    # other middlewares...
    'django_user_agents.middleware.UserAgentMiddleware',
    'django_ip_geolocation.middleware.IpGeolocationMiddleware',
)

# IP_GEOLOCATION_SETTINGS = {
#     'BACKEND': 'django_ip_geolocation.backends.IPStack',
#     'BACKEND_API_KEY': env('BACKEND_API_KEY'),
#     'BACKEND_EXTRA_PARAMS': {},
#     'BACKEND_USERNAME': '',
#     'RESPONSE_HEADER': 'X-IP-Geolocation',
#     'ENABLE_REQUEST_HOOK': True,
#     'ENABLE_RESPONSE_HOOK': True,
#     'ENABLE_COOKIE': False,
#     'FORCE_IP_ADDR': None,
#     'USER_CONSENT_VALIDATOR': None
# }



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.mysql',
#     #     'NAME': env('DB_NAME'),
#     #     'USER': env('DB_USER'),
#     #     'PASSWORD': env('DB_PASSWORD'),
#     #     'HOST': env('DB_HOST'),
#     #     'PORT': env('DB_PORT'),
#     # }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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




AUTH_PROFILE_MODULE = 'user.UserProfile'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIR = [
    Path(BASE_DIR, 'static')
]

#STATIC_ROOT = '/home/ubuntu/namaste_ongole/assets'  # Path(BASE_DIR, 'assets')
STATIC_ROOT = Path(BASE_DIR, 'assets')


MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')

#django_heroku.settings(locals())


# # RAZORPAY_CONFIGURATION
# RAZORPAY_KEY = env('RAZORPAY_KEY')
# RAZORPAY_SECRET = env('RAZORPAY_SECRET')
