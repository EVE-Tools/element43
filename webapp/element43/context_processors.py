from django.conf import settings

def element43_settings(request):
    """
    Adds element43 specific settings to the context.
    """
    return { 'IMAGE_SERVER' : settings.IMAGE_SERVER }