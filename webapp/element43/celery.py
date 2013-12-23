# Future imports
from __future__ import absolute_import

# Green the World!
import eventlet
eventlet.monkey_patch()

# OS import for loading environment later on
import os

# Import celery
from celery import Celery

# Import Django's settings
from django.conf import settings


# Set the default Django settings module for the 'celery' program. Defaults to production.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'element43.settings.production')

# Initialize Celery app
app = Celery('element43')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

# Load element43's apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)