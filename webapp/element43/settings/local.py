# Import base settings
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

IMAGE_SERVER = 'https://cdn.zweizeichen.org'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += (#'debug_toolbar',
                  #'devserver',
                  )

TEMPLATE_LOADERS = (
    'element43.template_loaders.DjamlFilesystemLoader',
    'element43.template_loaders.DjamlAppDirectoriesLoader',

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": "element43",
                "USER": "element43",
                "PASSWORD": "element43",
                "HOST": "localhost",
                "PORT": "",
            }
        }

# Memcache settings
MEMCACHE_SERVER = ['127.0.0.1']
MEMCACHE_BINARY = True
MEMCACHE_BEHAVIOUR = {"tcp_nodelay": True,
                      "ketama": True}

INTERNAL_IPS = ('127.0.0.1',)
