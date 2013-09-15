"""
Forms and validation code for user registration.

"""

from django.contrib.auth.models import User
from django import forms

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required form-control'}


class LoginForm(forms.Form):
    """
    Login form.
    """
    username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, widget=forms.TextInput(attrs=attrs_dict),
                                error_messages={'invalid': "Your username may contain only letters, numbers and @/./+/-/_ characters."})

    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))

    def clean(self):
        return self.cleaned_data


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    # Registration
    username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, widget=forms.TextInput(attrs=attrs_dict),
                                error_messages={'invalid': "Your username may contain only letters, numbers and @/./+/-/_ characters."})

    email = forms.EmailField(widget=forms.TextInput(attrs=attrs_dict))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
    password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password' in self.cleaned_data and 'password_repeat' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
                raise forms.ValidationError("The two password fields didn't match.")

        return self.cleaned_data


class ResetPasswordForm(forms.Form):
    """
    Form for resetting a given user's password.
    TODO: Add API ID field associated with this user/email combination to prevent unauthorized resets
    """
    # Reset data
    username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, widget=forms.TextInput(attrs=attrs_dict),
                                error_messages={'invalid': "The username may contain only letters, numbers and @/./+/-/_ characters."})

    email = forms.EmailField(widget=forms.TextInput(attrs=attrs_dict))

    def clean(self):

        try:
            user = User.objects.get(username__exact=self.cleaned_data.get('username'),
                                    email__exact=self.cleaned_data.get('email'))
        except:
            raise forms.ValidationError("There is no such account.")

        return self.cleaned_data
