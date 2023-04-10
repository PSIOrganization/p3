"""
Django settings for kahootclone project.

Generated by 'django-admin startproject' using Django 3.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

if 'TESTING' in os.environ:
    SECRET_KEY = 'django-insecure-7u$ha(4f3bpru)v8i+0qjgtm^zoz@50+9b#kzof+%^lq^&(9)m'
    DEBUG = 'DEBUG' in os.environ  # Only set to True if DEBUG is set
    ALLOWED_HOSTS = ['127.0.0.1']
else:
    # Only relevant in render deployment
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = 'RENDER' not in os.environ  # Only set to False in render
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

# do the thing with allowed hosts

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'models.apps.ModelsConfig',
    'services.apps.ServicesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'kahootclone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'kahootclone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# SQLite will not be used in producton or development, we will leave this code here but it is rectified later

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTH_USER_MODEL = 'models.User'  # This is the new default user model

LOGIN_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
# subject to change later depending on where we put them

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# To run the app locally, or use the tests: export TESTING=1
# To see the current value just type echo $TESTING

if 'TESTING' in os.environ:
    db_from_env = dj_database_url.config(
        default='postgres://alumnodb:alumnodb@localhost:5432/psi',
        conn_max_age=500)
else:
    # Use when deploy in render.com
    # db stored in env variable DATABASE_URL
    db_from_env = dj_database_url.config(default=os.getenv('DATABASE_URL'),
                                         conn_max_age=500)
DATABASES['default'].update(db_from_env)
# Update the default database with the new settings

# if 'TESTING' not in os.environ:
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'