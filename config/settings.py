import sys
import tempfile
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-i7d_4&2#m!ih$klw*sqfbl35_rwa3xdv76$5-0no%#)2fv4w(u'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'true').lower() == 'true'
PINIT_API_TOKEN = os.getenv('PINIT_API_TOKEN', None)
PINIT_API_BASE_URL = os.getenv('PINIT_API_BASE_URL', 'https://api.pinit.ch')

ALLOWED_HOSTS = os.getenv(
    'DJANGO_ALLOWED_HOSTS', '*'
).split(' ')

CSRF_TRUSTED_ORIGINS = os.getenv(
    'DJANGO_TRUSTED_ORIGINS', 'http://localhost:8000 http://127.0.0.1:8000'
).split(' ')

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'apps.shared',
    'apps.core',


    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect'
]

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
)

APP_ROLE = 'specific-role'
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_ONLY = True
SOCIALACCOUNT_ADAPTER = 'config.keycloak_adapter.KeycloakRoleAdapter'
KC_REALM = os.environ.get('KC_REALM', 'master')
KC_BASE_URL = os.environ.get('KC_BASE_URL', 'http://localhost:8080')
KC_CLIENT_ID = os.environ.get('KC_CLIENT_ID', 'web-app')
KC_CLIENT_SECRET = os.environ.get(
    'KC_CLIENT_ID', 'ki50FkYKHQRJV4yplwww0M15Pk912Qdz'
)
KC_REALM_URL = f'{KC_BASE_URL}/realms/{KC_REALM}'
KC_ISSUER = os.environ.get('KC_ISSUER', KC_REALM_URL)
SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "openid_connect",
                "name": "openid_connect",
                "client_id": KC_CLIENT_ID,
                "secret": KC_CLIENT_SECRET,
                "settings": {
                    "server_url": f"{KC_REALM_URL}/.well-known/openid-configuration",
                },
            }
        ]
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'config.middlewares.ThreadLocalMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

if DEBUG and 'test' not in sys.argv:
    INSTALLED_APPS.append(
        # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#install-the-app
        'debug_toolbar',
    )
    MIDDLEWARE = [
        # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-middleware
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': lambda request: True
    }

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(
            os.getenv('DJANGO_DB_DIR', BASE_DIR), 'db.sqlite3'
        ),
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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('fr', _('French')),
)

LOCALE_PATHS = [
    BASE_DIR / os.path.join('core', 'shared', 'i18n')
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = os.getenv('DJANGO_STATIC_DIR', 'static/')
STATIC_URL = 'static/'
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_DIR', 'media/')
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING_DIR = os.getenv('DJANGO_LOGGING_DIR', tempfile.gettempdir())
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGGING_DIR, 'portal.log'),
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

DEFAULT_PAGE_SIZE = 25

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Admin Panel",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Admin Panel",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Admin Panel",
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': DEFAULT_PAGE_SIZE,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'config.keycloak_authentication.KeycloakAuthentication',
    ],
}
