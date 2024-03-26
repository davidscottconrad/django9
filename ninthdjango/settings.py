"""
Django settings for ninthdjango project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import dj_database_url
from os import environ
import json
from environs import Env

env = Env()
env.read_env() 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
if "DATABASE_URL" in environ:
    secrets = environ.get("DATABASE_URL")
    SECRET_KEY = json.loads(secrets)["SECRET_KEY"]
    ALLOWED_HOSTS = [".awsapprunner.com", "https://www.netflax.me"]
    DEBUG = True

else: 
    SECRET_KEY = env('SECRET_KEY')
    ALLOWED_HOSTS=['*']
    DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninthdjango',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]



CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    'https://faanpz6hhp.us-east-2.awsapprunner.com',
    'https://main.dnbfl0efjxfzm.amplifyapp.com',
    "https://pyhnqwzimi.us-east-2.awsapprunner.com",
    'https://www.netflax.me',
]

ROOT_URLCONF = 'ninthdjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ninthdjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if "DATABASE_URL" in environ:
    db_url = json.loads(secrets)["DATABASE_URL"]
    DATABASES = {"default": dj_database_url.parse(db_url)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'usersdb', 
            'USER': 'admin', 
            'PASSWORD': 'mypassword',
            'HOST': 'db', 
            'PORT': '5432',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": 'storages.backends.s3boto3.S3Boto3Storage',
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if "DATABASE_URL" in environ:
    AWS_ACCESS_KEY_ID = json.loads(secrets)["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = json.loads(secrets)["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = json.loads(secrets)["AWS_STORAGE_BUCKET_NAME"]
else: 
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')