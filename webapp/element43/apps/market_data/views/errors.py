# Template and context-related imports
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# JSON for the live search
from django.utils import simplejson


def handler_403(request):
    
    """
    Redirects user home with an error message.
    """
    
    messages.warning(request, '403 - Forbidden. You were not supposed to access the page you tried to look at.')
    return HttpResponseRedirect(reverse('home'))

def handler_404(request):
    
    """
    Redirects user home with an error message.
    """
    
    messages.warning(request, '404 - The page you were looking for could not be found.')
    return HttpResponseRedirect(reverse('home'))
    
def handler_500(request):
    
    """
    Redirects user home with an error message.
    """
    
    messages.error(request, '500 - Internal server error. Looks like there is a bug in Element43. The error was logged and we will try to fix it soon.')
    return HttpResponseRedirect(reverse('home'))
    