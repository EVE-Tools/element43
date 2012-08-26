# Template and context-related imports
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from django.template import RequestContext

# Registration-related imports
from apps.market_data.forms import RegistrationForm
from django.contrib.auth.models import User

# Settings and e-mail
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

# Utility imports
import uuid
import datetime

def register(request):
	if request.method == 'POST': # If the form has been submitted...
		form = RegistrationForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			# Create user and send activation mail
			
			# Create user
			user = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
			user.is_staff = False
			user.is_active = False
			user.save()
			
			# Fill profile
			profile = user.get_profile()
			
			# Generate activation key
			email_key = uuid.uuid4().hex
			profile.activation_key = email_key
			profile.key_expires = datetime.datetime.now() + datetime.timedelta(days=2)
			
			# Store API information
			profile.api_valid = True
			profile.api_id = form.cleaned_data.get('api_id')
			profile.api_verification_code = form.cleaned_data.get('api_verification_code')
			
			# Save Profile
			profile.save()
			
			# Send activation mail
			text = get_template('mail/activation.txt')
			html = get_template('mail/activation.haml')
			
			mail_context = Context({'username':form.cleaned_data.get('username'), 'activation_key':email_key})
			
			text_content = text.render(mail_context)
			html_content = html.render(mail_context)
			
			message = EmailMultiAlternatives('Welcome to Element43!', text_content, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data.get('email')])
			message.attach_alternative(html_content, "text/html")
			message.send()
			
			# Redirect to success page
			return HttpResponseRedirect('/register/success/')
	else:
		form = RegistrationForm() # An unbound form

	rcontext = RequestContext(request, {})
	return render_to_response('auth/register.haml', {'form': form}, rcontext)
	
def registration_success(request):
	rcontext = RequestContext(request, {})
	return render_to_response('auth/registration_success.haml', rcontext)
	
def activate(request, key):
	# Check if there is a user with this key
	user = User.objects.filter(profile__activation_key = key)
	
	if user:
		user[0].is_active = True
		user[0].save()
		success = True
	else:
		success = False
		
	rcontext = RequestContext(request, {'success':success})
	return render_to_response('auth/activate.haml', rcontext)