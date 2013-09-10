import datetime
from django.db import models

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
    is_character_key = models.BooleanField(help_text="Is this a character key?  false = corporation key", default=True)
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
    dob = models.DateTimeField(help_text="DoB of character", default=datetime.datetime.now())
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
    cached_until = models.DateTimeField(help_text="data cached until", default=datetime.datetime.now())

    class Meta(object):
        verbose_name = "Character"
        verbose_name_plural = "Characters"


class CharSkill(models.Model):
    """
    Tracking skills
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
    character = models.ForeignKey('api.Character', help_text="FKey relationship to character table", null=True, default=None)
    corporation = models.ForeignKey('api.Corp', help_text="FKey relationship to corporation table", null=True, default=None)
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

    class Meta(object):
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


# Corporation
class Corp(models.Model):
    """
    Table for CorporationSheet information
    """

    corp_id = models.BigIntegerField(help_text="Corporation ID", db_index=True)
    name = models.TextField(help_text="Corporation name")
    ticker = models.TextField(help_text="Corp ticker")
    ceo_id = models.BigIntegerField(help_text="character ID of CEO")
    ceo_name = models.TextField(help_text="CEO Name")
    stastation = models.ForeignKey('eve_db.StaStation', help_text="Station corp headquarters is in")
    description = models.TextField(help_text="Description of corp if provided")
    url = models.TextField(help_text="URL for corporation")
    tax_rate = models.PositiveIntegerField(help_text="Tax rate of corporation")
    member_count = models.PositiveIntegerField(help_text="Number of members of corp")
    member_limit = models.PositiveIntegerField(help_text="Max number of members corp can support")
    shares = models.PositiveIntegerField(help_text="Number of shares of corp outstanding")

    class Meta(object):
        verbose_name = "Corporation"
        verbose_name_plural = "Corporations"


class CorpDivision(models.Model):
    """
    Divisions in a corp
    """

    corporation = models.ForeignKey('api.Corp', help_text="FK to corporation table")
    account_key = models.PositiveIntegerField(help_text="account key of corporation division")
    description = models.TextField(help_text="Name of division")


class CorpWalletDivision(models.Model):
    """
    Divisions in a corp
    """

    corporation = models.ForeignKey('api.Corp', help_text="FK to corporation table")
    account_key = models.PositiveIntegerField(help_text="account key of corporation wallet account division")
    description = models.TextField(help_text="Name of wallet account division")

class CorpPermissions(models.Model):
    """
    Permissions for corporations so multiple people can see corporation data
    """

    user = models.ForeignKey('auth.User', help_text="FKey relationship to user table")
    corporation = models.ForeignKey('api.Corp', help_text="FK to corporation table")
    character = models.ForeignKey('api.Character', help_text="FKey relationship to character table")
    view_wallet = models.BooleanField(help_text = "can view corporate wallet")
    view_transaction = models.BooleanField(help_text = "can view corporate transactions")
    view_research = models.BooleanField(help_text = "can view corporate research")
    modify_rights = models.BooleanField(help_text = "can modify corprate rights")

# Market Orders
class MarketOrder(models.Model):
    """
    This is the market order table off the CCP API
    """

    id = models.ForeignKey('market_data.Orders', primary_key=True, help_text="Unique key for this order, uses CCP order ID")
    character = models.ForeignKey('api.Character', help_text="FK relationship to character table", null=True, default=None)
    corporation = models.ForeignKey('api.Corp', help_text="FK relationship to corporation table", null=True, default=None)
    order_state = models.PositiveIntegerField(help_text="Valid states: 0 = open/active, 1 = closed, 2 = expired (or fulfilled), 3 = cancelled, 4 = pending, 5 = character deleted")
    account_key = models.PositiveIntegerField(help_text="Which division this order is using as its account. Always 1000 for characters, but in the range 1000 to 1006 for corporations.")
    escrow = models.FloatField(help_text="Escrow amount for this order")

    class Meta(object):
        verbose_name = "API Market Order"
        verbose_name_plural = "API Market Orders"


# RefTypes for journal entries
class RefType(models.Model):
    """
    This provides descriptions for the diffrent RefTypes.
    """

    id = models.PositiveIntegerField(help_text="Unique refTypeID from API.", primary_key=True)
    name = models.TextField(help_text="Name of this refType")

    class Meta(object):
        verbose_name = "API RefTypeID to name mapping"
        verbose_name_plural = "API RefTypeID to name mappings"


# JournalEntries
class JournalEntry(models.Model):
    """
    Stores char/corp journal entries.
    """

    ref_id = models.BigIntegerField(help_text="Unique refID from CCP for this journal entry. Not primary key - multiple characters could have access to a single corporation's wallet API.")
    character = models.ForeignKey('api.Character', help_text="FK relationship to character table", null=True, default=None)
    corporation = models.ForeignKey('api.Corp', help_text="FK relationship to corporation table", null=True, default=None)
    date = models.DateTimeField(help_text="Date and time of the transaction.")
    ref_type = models.ForeignKey('api.RefType', help_text="Transaction type FKey relationship.")
    amount = models.FloatField(help_text="Amount transferred between parties.")
    balance = models.FloatField(help_text="Balance in this wallet after this transaction.")
    owner_name_1 = models.TextField(help_text="Name of first party in the transaction.")
    owner_id_1 = models.BigIntegerField(help_text="Character or corporation ID of the first party.")
    owner_name_2 = models.TextField(help_text="Name of second party in the transaction.")
    owner_id_2 = models.BigIntegerField(help_text="Character or corporation ID of the second party.")
    arg_name_1 = models.TextField(help_text="Has different meanings - see: http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML#Arguments")
    arg_id_1 = models.PositiveIntegerField(help_text="Has different meanings - see: http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML#Arguments")
    reason = models.TextField(help_text="Has different meanings - see: http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML#Arguments")
    tax_receiver_id = models.BigIntegerField(help_text="CorpID who received tax for this transaction.")
    tax_amount = models.FloatField(help_text="Amount of tax for this transaction.")

    class Meta(object):
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"


# MarketTransaction
class MarketTransaction(models.Model):
    """
    Stores char/corp market transactions.
    """

    character = models.ForeignKey('api.Character', help_text="FK relationship to character table", null=True, default=None)
    corporation = models.ForeignKey('api.Corp', help_text="FK relationship to corporation table", null=True, default=None)
    date = models.DateTimeField(help_text="Date and time of the transaction.")
    transaction_id = models.BigIntegerField(help_text="Non-unique transaction ID.")
    invtype = models.ForeignKey('eve_db.InvType', help_text="The item traded in this transaction.")
    quantity = models.IntegerField(help_text="Number of items bought/sold.")
    price = models.FloatField(help_text="Price per unit of the item.")
    client_id = models.BigIntegerField(help_text="Character or corporation ID of the other party.")
    client_name = models.TextField(help_text="Name of other party.")
    station = models.ForeignKey('eve_db.StaStation', help_text="Station the transaction took place at.")
    is_bid = models.BooleanField(help_text="Marks whether this item was bought or sold.")
    is_corporate_transaction = models.BooleanField(help_text="Marks whether this is a corporate or a personal transaction.")
    journal_transaction_id = models.BigIntegerField(help_text="Journal refID for this transaction.")

    class Meta(object):
            verbose_name = "Market Transaction"
            verbose_name_plural = "Market Transactions"


# Character Research
class Research(models.Model):
    """
    Stores research jobs.
    """

    character = models.ForeignKey('api.Character', help_text="Character who owns this job.")
    agent = models.ForeignKey('eve_db.AgtAgent', help_text="The agent.")
    skill = models.ForeignKey('api.Skill', help_text="The skill used for the research.")
    start_date = models.DateTimeField(help_text="The date the character began the current research with the agent at the current points per day.")
    points_per_day = models.FloatField(help_text="The number of points generated per day.")
    remainder_points = models.FloatField(help_text="The number of points remaining since last datacore purchase and/or points_per_day update.")

    class Meta(object):
            verbose_name = "Research Job"
            verbose_name_plural = "Research Jobs"
