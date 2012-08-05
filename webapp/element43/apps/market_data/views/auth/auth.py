# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

def register(request):
	rcontext = RequestContext(request, {})
	return render_to_response('auth/register.haml', rcontext)