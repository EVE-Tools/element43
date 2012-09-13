from django.db import models

#
# Character information
#

class APIKey(models.Model):
    """
    Holds API information for a user.  One to many with user table.
    """
    
    keyid = models.PositiveIntegerField(help_text = "keyID for this character")
    vcode = models.TextField(help_text = "vCode for this key")
    expires = models.DateTimeField(help_text = "Expiry date for the key")
    accessmask = models.BigIntegerField(help_text="Access mask for this key")
    is_valid = models.BooleanField(help_text="Is this key valid?")
    
    class Meta(object):
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
    

class Character(models.Model):
    """
    Holds information specific to a character.  This is a one-to-many relationship between users & characters
    (ie, a user can have multiple characters, but a character can only have one user).  This stores API key information
    and other useful character-specific info.
    """
    
    id = models.BigIntegerField(primary_key=True,
                                help_text="Unique key for this character, uses CCP character ID")
    name = models.TextField(help_text="Character name")
    user = models.ForeignKey('auth.User', help_text="FKey relationship to user table")
    
    class Meta(object):
        verbose_name = "Character"
        verbose_name_plural = "Characters"
    
#
# API table
#

class APITimer(models.Model):
    """
    Tracking API timers
    """
    character = models.ForeignKey('api.Character', help_text="FKey relationship to character table")
    apisheet = models.TextField(help_text="Filename of API Call sheet")
    nextupdate = models.DateTimeField(help_text = "Date/Time of next allowed API refresh")
    
    class Meta(object):
        verbose_name="API Timer"
        verbose_name_plural = "API Timers"
