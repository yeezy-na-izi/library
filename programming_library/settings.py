import os
from pathlib import Path
from django.contrib.messages import constants as messages

import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://eec691dd2e5a48b0a58396faac2dc5bd@o1122268.ingest.sentry.io/6248932",
    integrations=[DjangoIntegration()],

    traces_sample_rate=1.0,
    send_default_pii=True
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-3pxc%b7_a2klsr^&4oe#288a32@@rdqk7dr-$v6wfo+!mzyy8!'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'programming-library-db.herokuapp.com']

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'https://programming-library-db.herokuapp.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library.apps.LibraryConfig',
    'user.apps.UserConfig'
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

ROOT_URLCONF = 'programming_library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_tags': 'library.tags',
            }
        },
    },
]

WSGI_APPLICATION = 'programming_library.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dadq44le9bfjk0',
        'USER': 'trninxplivcdeq',
        'PASSWORD': 'bba4c7ac606071e24efda2153d9fa1d17bd1cf15c891bd26906fb82a1406e5f2',
        'HOST': 'ec2-63-33-14-215.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
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

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

AUTH_USER_MODEL = 'user.CustomUser'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = 'static_root/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_HOST_USER = 'no_reply.library@extroot.ru'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'xHdYazhE9TXaKjY'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreplay.proglibrary@gmail.com'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = '3ref2RGrcVp74BS'

django_heroku.settings(locals())
