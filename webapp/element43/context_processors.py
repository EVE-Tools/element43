from django.conf import settings

def element43_settings(request):
    return { 'IMAGE_SERVER' : settings.IMAGE_SERVER }