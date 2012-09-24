# Template and context-related imports
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Models
from django.contrib.auth.models import User

# API Models
from apps.api.models import APIKey, Character

# Forms
from apps.market_data.forms.settings import ProfileForm, APIKeyForm

# Utility imports
import datetime

# API
from element43 import eveapi

@login_required
def settings(request):
	rcontext = RequestContext(request, {})
	return render_to_response('settings/settings.haml', rcontext)

@login_required
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
	
@login_required
def characters(request):
	characters = Character.objects.filter(user = request.user)
	
	if not characters:
		# Message and redirect
		messages.info(request, 'Currently there are no characters associated with your account. You need to add them via an API key first.')
		return HttpResponseRedirect('/settings/api/key/')
		
	rcontext = RequestContext(request, {'characters': characters})
	return render_to_response('settings/characters.haml', rcontext)

@login_required
def remove_character(request, char_id):
	try:
		# Delete only matching character to prevent unauthorized deletions
		char = Character.objects.get(user = request.user, id = char_id)
		char.delete()
	except:
		# Message and redirect
		messages.error(request, 'There is no such character.')
		return HttpResponseRedirect('/settings/characters/')
		
	# Message and redirect
	messages.info(request, 'Character was removed.')
	return HttpResponseRedirect('/settings/characters/')

@login_required
def api_key(request):
	# Get Keys
	keys = APIKey.objects.filter(user = request.user)
	
	# Form
	if request.method == 'POST':
		form = APIKeyForm(request.POST)
		if form.is_valid():
			
			# Add success message
			messages.success(request, 'Your key is valid. Please select the characters you want to add.')
			# Redirect home
			return HttpResponseRedirect('/settings/api/character/' + str(form.cleaned_data.get('api_id')) + '/' + form.cleaned_data.get('api_verification_code') + '/')
	else:
		form = APIKeyForm()

	rcontext = RequestContext(request, {})
	return render_to_response('settings/api_key.haml', {'form': form, 'keys': keys}, rcontext)

@login_required	
def remove_api_key(request, apikey_id):
	try:
		# Delete only matching character to prevent unauthorized deletions
		key = APIKey.objects.get(user = request.user, keyid = apikey_id)
		key.delete()
	except:
		# Message and redirect
		messages.error(request, 'There is no such key.')
		return HttpResponseRedirect('/settings/api/key/')
		
	# Message and redirect
	messages.info(request, 'The key and all associated characters were removed.')
	return HttpResponseRedirect('/settings/api/key/')

@login_required
def api_character(request, api_id, api_verification_code):
	
	"""
	Validate key / ID combination. If it's valid, check security bitmask.
	"""
	
	# Try to authenticate with supplied key / ID pair and fetch api key meta data.
	try:
		# Fetch info
		api = eveapi.EVEAPIConnection()
		auth = api.auth(keyID=api_id, vCode=api_verification_code)
		key_info = auth.account.APIKeyInfo()
	except:
		# Message and redirect
		messages.error(request, "Verification of your API key failed. Please follow the instructions on the right half of this page to generate a valid one.")
		return HttpResponseRedirect('/settings/api/key/')
			
	# Now check the access mask
	min_access_mask = 6361219
	
	# Do a simple bitwise operation to determine if we have sufficient rights with this key.
	if not ((min_access_mask & key_info.key.accessMask) == min_access_mask):
		# Message and redirect
		messages.error(request, "The API key you supplied does not have sufficient rights. Please follow the instructions on the right half of this page to generate a valid one.")
		return HttpResponseRedirect('/settings/api/key/')
		
	# Get characters associated with this key
	characters = auth.account.Characters().characters
	
	# If form is submitted, add characters to account
	if request.method == 'POST':
		post_characters = request.POST.getlist('characters')
		
		added_chars = False
		
		for char in characters:
			if str(char.characterID) in post_characters:
				# Add key to DB if it does not exist
				if not APIKey.objects.filter(keyid = api_id, vcode = api_verification_code):
					
					# Handle keys which never expire
					if len(key_info.key.expires) == 0:
						key_expiration = "9999-12-31 00:00:00"
					else:
						key_expiration = key_info.key.expires
						
					key = APIKey(user = request.user, keyid = api_id, vcode = api_verification_code, expires = key_expiration, accessmask = key_info.key.accessMask, is_valid = True)
					key.save()
				
				# Add character
				new_char = Character(id = char.characterID, name = char.name, user = request.user, apikey = key)
				new_char.save()
				
				added_chars = True
				
			# Change message depending on what we did
			if added_chars:
				messages.success(request, "Successfully added the selected character(s) to your account.")
			else:
				messages.info(request, "No characters were added.")
			return HttpResponseRedirect('/settings/characters/')
			
	rcontext = RequestContext(request, {'chars': characters})
	return render_to_response('settings/api_character.haml', rcontext)
	
	
