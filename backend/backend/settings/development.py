"""
Development-specific Django settings.
"""

from .base import *  # noqa: F401, F403

# ==================================================
# Debug
# ==================================================

DEBUG = True

# ==================================================
# Database - PostgreSQL with fallback to SQLite3 for dev
# ==================================================

import os
import socket
import sys

def is_postgres_available(host, port, timeout=1):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except Exception:
        return False

db_host = os.getenv('DB_HOST', '127.0.0.1')
db_port = os.getenv('DB_PORT', '5432')

if is_postgres_available(db_host, db_port):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'weather_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': db_host,
            'PORT': db_port,
        }
    }
else:
    print("WARNING: PostgreSQL is not reachable at {}:{}. Gracefully falling back to SQLite3 for development.".format(db_host, db_port), file=sys.stderr)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==================================================
# Email - Console backend for development
# ==================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==================================================
# CORS - Allow all in development
# ==================================================

CORS_ALLOW_ALL_ORIGINS = True

# ==================================================
# Django REST Framework - Add browsable API in dev
# ==================================================

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]

# ==================================================
# Channel Layers - In-memory for development
# ==================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

# ==================================================
# Cache - Local memory for development
# ==================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'weather-dev-cache',
    }
}

# ==================================================
# Static Files
# ==================================================

STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
