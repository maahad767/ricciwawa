"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import io
from pathlib import Path
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
from google.cloud import secretmanager

BASE_DIR = Path(__file__).resolve().parent.parent
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(BASE_DIR, 'ricciwawa-6e11b342c999.json')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+(qgy3*el_%em1s*r+!-ao95hyl!5mqe0g=5cj^3)@(w_2vw0v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',
    'dry_rest_permissions',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_elasticsearch_dsl',
    'djstripe',
    'cloudtask',

    # local apps
    'account',
    'post',
    'quiz',
    'web',
    'system',

    # reusable local apps
    'firebase_auth',
    'utils',
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ricciwawadevdb',
        'USER': 'ricciwawadevuser',
        'PASSWORD': 'lkCLt2sKmODpoNEe',
        'HOST': '127.0.0.1',
        'PORT': '5555',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = '/static/'
MEDIA_ROOT = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'firebase_auth.authentication.FirebaseAuthentication',  # includes firebase authentication
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}


# Change default auth user model
AUTH_USER_MODEL = 'account.User'


# Google Cloud Storage (For Static & Media Files) Settings
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'ricciwawa'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'  # Storage backend for static files
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'

# Schema Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'RICCIWAWA APIs',
    'DESCRIPTION': 'API for RICCIWAWA',
    'VERSION': '1.0.0',
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    }
}

# STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_51FW4RBD9iHs4oFDOa4CqRyDgXFB4fkrdWMJxJRlbjtsLfvf5t7uLEss9ebDvIMeG3YNgmZ6bz0C93s6MA8psOqE8000TWde3mg")
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_eY8QU7v9ffSqRcF41HT3dlmxJ7RpdN0Z"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True


# Elasticsearch configuration
CLOUD_ID = "RICCIWAWA:YXNpYS1lYXN0MS5nY3AuZWxhc3RpYy1jbG91ZC5jb20kOTNlMWIwMTQzM2RjNGY3YmE1OWM2YTk5MGNmNTk1OGUkNWU4ZjU5MTdmNGViNDQ0M2ExNmU5OTc2ZTgzNjY3Y2Y="
HTTP_AUTH = ("elastic", "srkMulf2O2XNEOiiQxcIH733")

ELASTICSEARCH_DSL = {
    'default': {
        'cloud_id': CLOUD_ID,
        'http_auth': HTTP_AUTH
    }
}
# CELERY CONFIG

if os.environ.get('DEBUG') == 'FALSE':
    DEBUG = False
else:
    DEBUG = True

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")

if os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    env.read_env(io.StringIO(payload))

    # Use django-environ to parse the connection string
    DATABASES = {"default": env.db()}

    # If the flag as been set, configure to use proxy
    if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
        DATABASES["default"]["HOST"] = "127.0.0.1"
        DATABASES["default"]["PORT"] = 5555

    CLOUDTASK: dict = {
        'PROJECT': project_id,
        'LOCATION': 'us-central1',
        'SAE': 'gaeinittest@appspot.gserviceaccount.com',
        'QUEUE': 'djangotestqueue',
        'URL': 'https://gaeinittest.uc.r.appspot.com/_tasks/',
        'SECRET': SECRET_KEY,
    }
else:
    raise Exception("No GOOGLE_CLOUD_PROJECT  detected. No secrets found.")
