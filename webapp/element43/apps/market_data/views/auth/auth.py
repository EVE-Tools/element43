# Template and context-related imports
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from django.template import RequestContext
from django.contrib import messages

# Authentication
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

# Registration-related imports
from apps.market_data.forms.auth import RegistrationForm
from apps.market_data.forms.auth import ResetPasswordForm
from apps.market_data.forms.auth import LoginForm
from django.contrib.auth.models import User

# Settings and e-mail
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

# Utility imports
import uuid
import datetime
from urlparse import urlparse, urlunparse

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
        
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    # Add success message
                    messages.success(request, 'Hello ' + user.username + '! You were logged in successfully.')
                    
                    # Redirection
                    # Default to default
                    redirect_to = request.REQUEST.get('next', '')
                    
                    if redirect_to:
                        netloc = urlparse(redirect_to)[1]
                        # Heavier security check -- don't allow redirection to a different
                        # host.
                        if netloc and netloc != request.get_host():
                            # Warn user
                            messages.warning(request, 'External login redirect URL detected! It looks like someone tried to trick you. Do not trust the person who gave you this link!')
                            redirect_to = settings.LOGIN_REDIRECT_URL
                           
                    else:
                        redirect_to = settings.LOGIN_REDIRECT_URL
                        
                    return HttpResponseRedirect(redirect_to)
                
                else:
                    # Add error message
                    messages.error(request, 'Your account is not active.')
                
            else:
                # Add error message
                messages.error(request, 'Incorrect username or password. Try again!')
    else:
        form = LoginForm()
  
    rcontext = RequestContext(request, {})
    return render_to_response('auth/login.haml', {'form': form}, rcontext)
    
def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
        # Redirect
        messages.info(request, 'You were logged out successfully.')
    return HttpResponseRedirect(reverse('home'))

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
            email_key = user.username + uuid.uuid4().hex
            profile.activation_key = email_key
            profile.key_expires = datetime.datetime.now() + datetime.timedelta(days=2)
            
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
            
            # Add success message
            messages.success(request, 'Your account has been created and an e-mail message containing your activation key has been sent to the address you specified. You have to activate your account within the next 48 hours.')
            # Redirect home
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegistrationForm() # An unbound form

    rcontext = RequestContext(request, {})
    return render_to_response('auth/register.haml', {'form': form}, rcontext)

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
    
        if form.is_valid():
            # Generate and save password
            new_password = User.objects.make_random_password(length=12, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            user = User.objects.get(username__exact = form.cleaned_data.get('username'), email__exact = form.cleaned_data.get('email'))
            
            user.set_password(new_password)
            user.save()
            
            # Send password reset mail
            text = get_template('mail/reset_password.txt')
            html = get_template('mail/reset_password.haml')
            
            mail_context = Context({'username':form.cleaned_data.get('username'), 'new_password':new_password})
            
            text_content = text.render(mail_context)
            html_content = html.render(mail_context)
            
            message = EmailMultiAlternatives('Element43 password reset', text_content, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data.get('email')])
            message.attach_alternative(html_content, "text/html")
            message.send()
            
            # Add success message
            messages.info(request, 'A new password has been sent to your e-mail address.')
            # Redirect home
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ResetPasswordForm()
  
    rcontext = RequestContext(request, {})
    return render_to_response('auth/reset_password.haml', {'form': form}, rcontext)
    
def registration_success(request):
    rcontext = RequestContext(request, {})
    return render_to_response('auth/registration_success.haml', rcontext)
    
def activate(request, key):
    # Check if there is a user with this key
    user = User.objects.filter(profile__activation_key = key)
    
    if user:
        # Activate user
        user[0].is_active = True
        user[0].save()
        
        # Add error message
        messages.success(request, 'Thank you for activating you account. You can use all features of Element43 now!')
    else:
        # Add success message
        messages.error(request, 'There is no account associated with this key!')
    
    # Redirect home
    return HttpResponseRedirect(reverse('home'))
        
    rcontext = RequestContext(request, {'success':success})
    return render_to_response('auth/activate.haml', rcontext)
