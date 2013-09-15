"""
Forms and validation code for user settings.
"""

from django.contrib.auth.models import User
from django import forms

# Authentication
from django.contrib.auth import authenticate

# API
from element43 import eveapi

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required form-control'}


class ProfileForm(forms.Form):
    """
    Allows the user to change the profile.
    """

    # Registration
    email = forms.EmailField(widget=forms.TextInput(attrs=attrs_dict), required=False)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
    new_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), required=False)
    new_password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

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
        # Check if old password is right
        if 'password' in self.cleaned_data:
            if authenticate(username=self.request.user.username, password=self.cleaned_data['password']) is None:
                raise forms.ValidationError("Wrong password.")

        # Check if new passwords match
        if 'new_password' in self.cleaned_data and 'new_password_repeat' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['new_password_repeat']:
                raise forms.ValidationError("The two password fields didn't match.")

        return self.cleaned_data


class APIKeyForm(forms.Form):
    """
    API key submission form.
    """

    # API Key
    api_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'span2 required form-control'}))
    api_verification_code = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))

    def clean(self):

        """
        Validate key / ID combination. If it's valid, check security bitmask.
        """
        api_id = self.cleaned_data.get("api_id")
        api_verification_code = self.cleaned_data.get("api_verification_code")

        # Try to authenticate with supplied key / ID pair and fetch api key meta data.
        try:
            # Fetch info
            api = eveapi.EVEAPIConnection()
            auth = api.auth(keyID=api_id, vCode=api_verification_code)
            key_info = auth.account.APIKeyInfo()
        except:
            raise forms.ValidationError("Verification of your API key failed. Please follow the instructions on the right half of this page to generate a valid one.")

        return self.cleaned_data
