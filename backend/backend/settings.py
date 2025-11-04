from pathlib import Path
from datetime import timedelta
import os
import re
import dj_database_url

# Load environment variables solo en desarrollo (no en Railway)
if not os.getenv('RAILWAY_ENVIRONMENT'):
    from dotenv import load_dotenv
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-change-in-production')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Permitir todos los hosts en Railway (usará *.railway.app)
if os.getenv('RAILWAY_ENVIRONMENT'):
    ALLOWED_HOSTS = ['*']  # Railway maneja el routing
else:
    ALLOWED_HOSTS = os.getenv(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'users',
    'games',
    'content',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database Configuration
# Usar PostgreSQL en producción, SQLite en desarrollo
database_url = os.getenv('DATABASE_URL') or os.getenv('DATABASE_PUBLIC_URL')

if database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
# Usar Railway Volume en producción o local en desarrollo
if os.getenv('RAILWAY_ENVIRONMENT'):
    # En producción, usar el volumen montado en /app/media
    MEDIA_ROOT = '/app/media'
    MEDIA_URL = '/media/'
else:
    # En desarrollo local
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Settings
# Permitir origenes específicos
cors_origins_env = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
)
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(',') if origin.strip()]

# Permitir todos los subdominios de Vercel para preview deployments
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",  # Cualquier subdominio de vercel.app
]

CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins (para admin y formularios en producción)
csrf_origins_env = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
)
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_env.split(',') if origin.strip()]

# Añadir también subdominios de Vercel dinámicamente si es necesario
if os.getenv('RAILWAY_ENVIRONMENT'):
    # En producción, permitir cualquier subdominio de vercel.app para CSRF
    CSRF_TRUSTED_ORIGINS.extend([
        'https://game-xy.vercel.app',
        'https://*.vercel.app',  # Django 4.0+ soporta wildcards en CSRF
    ])

# Security Settings for Production
if not DEBUG:
    # No forzar SSL redirect en Railway (usa su proxy)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Permitir acceso al healthcheck sin slash redirect
APPEND_SLASH = True
