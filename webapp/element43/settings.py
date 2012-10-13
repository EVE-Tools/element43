# Django settings for element43 project.
import os
import sys
import djcelery

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# This is the 'webapp' dir, AKA the webapp project root.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the 'element43' module to the path.
sys.path.insert(0, os.path.join(ROOT_DIR, 'element43'))

# fire up celery
BROKER_URL = 'redis://localhost'
djcelery.setup_loader()

# Our User profile class
AUTH_PROFILE_MODULE = 'common.Profile'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# E-Mail settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no_reply@element-43.com'

# Login
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

MANAGERS = ADMINS

RAVEN_CONFIG = {
    'dsn': 'http://public:secret@example.com/1',
}

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

# Store flash messages in session
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

# Compression
COMPRESS_ENABLED = False
COMPRESS_ROOT = os.path.join(ROOT_DIR, 'assets')
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = [
     'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
     'compressor.filters.jsmin.JSMinFilter'
]

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_DIR, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f%is=((x7m^f&amp;^s1_oy*p#8don$g%stq+=p5#+a7x^nof1^%0y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (

    'element43.template_loaders.DjamlFilesystemLoader',
    'element43.template_loaders.DjamlAppDirectoriesLoader',

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

# Template Context processors
TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.request",
        "django.core.context_processors.csrf",
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "element43.context_processors.element43_settings",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Catch 404s with sentry
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'element43.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'element43.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.formtools',

    'compressor',

    'raven.contrib.django',

    'south',
    'devserver',
    'djcelery',

    'eve_db',
    'apps.common',
    'apps.market_data',
    'apps.api',
    'apps.auth',
    'apps.user_settings',
    'apps.manufacturing',
)

DEVSERVER_MODULES = (
    #'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    #'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    #'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    #'devserver.modules.cache.CacheSummaryModule',
    #'devserver.modules.profile.LineProfilerModule',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

IMAGE_SERVER = 'http://images.element-43.com'
MEMCACHE_SERVER = '127.0.0.1'

# This allows you to override these settings without modifying the defaults.
# Create a local_settings.py file and copy/paste/modify things from here.
try:
    from local_settings import *
except ImportError:
    pass
