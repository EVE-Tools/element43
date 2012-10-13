from django.db import models
from datetime import datetime

#
# Character information
#


class APIKey(models.Model):
    """
    Holds API information for a user.  One to many with user table.
    """

    keyid = models.PositiveIntegerField(help_text="keyID for this character")
    vcode = models.TextField(help_text="vCode for this key")
    expires = models.DateTimeField(help_text="Expiry date for the key")
    accessmask = models.BigIntegerField(help_text="Access mask for this key")
    is_valid = models.BooleanField(help_text="Is this key valid?")
    user = models.ForeignKey('auth.User', help_text="Fkey relationship to user table")

    class Meta(object):
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"


class Character(models.Model):
    """
    Holds information specific to a character.  This is a one-to-many relationship between users & characters
    (ie, a user can have multiple characters, but a character can only have one user).  This stores API key information
    and other useful character-specific info.
    """

    id = models.BigIntegerField(primary_key=True, help_text="Unique key for this character, uses CCP character ID")
    name = models.TextField(help_text="Character name")
    user = models.ForeignKey('auth.User', help_text="FKey relationship to user table")
    apikey = models.ForeignKey('api.APIKey', help_text='FKey relationship to api key table')
    name = models.TextField(help_text="Name of character")
    dob = models.DateTimeField(help_text="DoB of character", default=datetime.now())
    race = models.TextField(help_text="Race of character", default="")
    bloodline = models.TextField(help_text="Bloodline of character", default="")
    ancestry = models.TextField(help_text="Ancestry of character", default="")
    gender = models.TextField(help_text="Gender", default="Male")
    corp_name = models.TextField(help_text="Name of corporation character is member of", default="")
    corp_id = models.BigIntegerField(help_text="id of corporation", default=0)
    alliance_name = models.TextField(help_text="Name of alliance", default="")
    alliance_id = models.BigIntegerField(help_text="id of alliance", default=0)
    clone_name = models.TextField(help_text="clone level name", default="")
    clone_skill_points = models.PositiveIntegerField(help_text="max SP of clone", default=0)
    balance = models.BigIntegerField(help_text="isk on hand", default=0)
    implant_memory_name = models.TextField(help_text="name of memory implant", default="")
    implant_memory_bonus = models.PositiveIntegerField(help_text="memory bonus", default=0)
    implant_intelligence_name = models.TextField(help_text="name of intelligence implant", default="")
    implant_intelligence_bonus = models.PositiveIntegerField(help_text="intelligence bonus", default=0)
    implant_charisma_name = models.TextField(help_text="name of charisma implant", default="")
    implant_charisma_bonus = models.PositiveIntegerField(help_text="charisma bonus", default=0)
    implant_willpower_name = models.TextField(help_text="name of willpower implant", default="")
    implant_willpower_bonus = models.PositiveIntegerField(help_text="willpower bonus", default=0)
    implant_perception_name = models.TextField(help_text="name of perception implant", default="")
    implant_perception_bonus = models.PositiveIntegerField(help_text="perception bonus", default=0)
    cached_until = models.DateTimeField(help_text="data cached until", default=datetime.now())

    class Meta(object):
        verbose_name = "Character"
        verbose_name_plural = "Characters"


class CharSkill(models.Model):
    """
    Trackign skills
    """
    character = models.ForeignKey('api.Character', help_text="FKey relationship to character table")
    skill = models.ForeignKey('api.Skill', help_text="FK relationship to skill table")
    skillpoints = models.PositiveIntegerField(help_text="SP trained")
    level = models.PositiveIntegerField(help_text="level trained")

#
# API table
#


class APITimer(models.Model):
    """
    Tracking API timers
    """
    character = models.ForeignKey('api.Character', help_text="FKey relationship to character table")
    apisheet = models.TextField(help_text="Filename of API Call sheet")
    nextupdate = models.DateTimeField(help_text="Date/Time of next allowed API refresh")

    class Meta(object):
        verbose_name = "API Timer"
        verbose_name_plural = "API Timers"

#
# Skill tree
#


class SkillGroup(models.Model):
    """
    This is the global eve skill groups
    """

    id = models.PositiveIntegerField(help_text="Group ID from API", primary_key=True)
    name = models.TextField(help_text="Name of skill group")

    class Meta(object):
        verbose_name = "Skill Group"
        verbose_name_plural = "Skill Groups"


class Skill(models.Model):
    """
    This is the global Eve skill tree
    """

    id = models.PositiveIntegerField(help_text="Skill ID from API", primary_key=True)
    name = models.TextField(help_text="Name of skill")
    group = models.ForeignKey('api.SkillGroup', help_text="FK to skill group")
    published = models.BooleanField(help_text="Published flag")
    description = models.TextField(help_text="description of skill")
    rank = models.PositiveIntegerField(help_text="skill difficulty rank")
    primary_attribute = models.TextField(help_text="Primary attribute for skill")
    secondary_attribute = models.TextField(help_text="secondary attribute for skill")
