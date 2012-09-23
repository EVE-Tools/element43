# Template and context-related imports
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from django.template import RequestContext
from django.contrib import messages

# API Models

# Registration-related imports
from apps.market_data.forms.settings import ProfileForm
from django.contrib.auth.models import User

# Utility imports
import datetime
	
def settings(request):
	rcontext = RequestContext(request, {})
	return render_to_response('settings/settings.haml', rcontext)
	
def profile(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST, request = request)
		if form.is_valid(): 
			
			# Change email
			if form.cleaned_data.get('email'):
				request.user.email = form.cleaned_data.get('email')
				
			# Change Password
			if form.cleaned_data.get('new_password'):
				request.user.set_password(form.cleaned_data.get('new_password'))
			
			request.user.save()
			
			# Add success message
			messages.success(request, 'Saved new profile data.')
			# Redirect home
			return HttpResponseRedirect('/settings/')
	else:
		form = ProfileForm(request = request)

	rcontext = RequestContext(request, {})
	return render_to_response('settings/settings.haml', {'form': form}, rcontext)
	

def characters(request):
	rcontext = RequestContext(request, {})
	return render_to_response('settings/characters.haml', rcontext)

def api_key(request):
	rcontext = RequestContext(request, {})
	return render_to_response('settings/api_key.haml', rcontext)

def api_characters(request):
	rcontext = RequestContext(request, {})
	return render_to_response('settings/settings.haml', rcontext)
	
