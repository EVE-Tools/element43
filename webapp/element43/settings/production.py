# Import base settings
from .base import *

# Default configuration
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Fire up celery
BROKER_URL = 'redis://localhost'
djcelery.setup_loader()

# E-Mail settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no_reply@element-43.com'

# Config for sentry
RAVEN_CONFIG = {
    'dsn': get_env_variable('E43_RAVEN_URL'),
}

# Google Analytics
GOOGLE_ANALYTICS_ENABLED = False
GOOGLE_ANALYTICS_TRACKING_ID = 'UA-36064829-1'
GOOGLE_ANALYTICS_DOMAIN_NAME = 'element-43.com'

# Compression
COMPRESS_ENABLED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'element43',
        'USER': 'element43',
        'PASSWORD': '',
        # Set to empty string for localhost.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('E43_SECRET_KEY')

# Memcache settings
MEMCACHE_SERVER = ['127.0.0.1']
MEMCACHE_BINARY = True
MEMCACHE_BEHAVIOUR = {"tcp_nodelay": True,
                      "ketama": True}

# Configure sentry
INSTALLED_APPS += ('raven.contrib.django',)
MIDDLEWARE_CLASSES += ('raven.contrib.django.middleware.Sentry404CatchMiddleware',)