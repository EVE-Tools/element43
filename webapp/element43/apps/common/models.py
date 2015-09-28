"""
Model definitions for storing user profiles.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#
# User Profile
#


class Profile(models.Model):
    """
    Holds additional profile fields of every User like the API keys.
    """
    # Link to User
    user = models.OneToOneField(User)

    # Registration and profile data
    activation_key = models.CharField(max_length=255,
                                      help_text="E-mail activation key.")
    key_expires = models.DateTimeField(null=True,
                                       help_text="Expiration date of activation key.")

    class Meta(object):
            verbose_name = "User Profile"
            verbose_name_plural = "User Profiles"


def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler for creating a profile when users are created
    """

    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
