# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyid', models.PositiveIntegerField(help_text=b'keyID for this character')),
                ('vcode', models.TextField(help_text=b'vCode for this key')),
                ('expires', models.DateTimeField(help_text=b'Expiry date for the key')),
                ('accessmask', models.BigIntegerField(help_text=b'Access mask for this key')),
                ('is_valid', models.BooleanField(help_text=b'Is this key valid?')),
                ('is_character_key', models.BooleanField(default=True, help_text=b'Is this a character key?  false = corporation key')),
            ],
            options={
                'verbose_name': 'API Key',
                'verbose_name_plural': 'API Keys',
            },
        ),
        migrations.CreateModel(
            name='APITimer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apisheet', models.TextField(help_text=b'Filename of API Call sheet')),
                ('nextupdate', models.DateTimeField(help_text=b'Date/Time of next allowed API refresh')),
            ],
            options={
                'verbose_name': 'API Timer',
                'verbose_name_plural': 'API Timers',
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigIntegerField(help_text=b'Unique key for this character, uses CCP character ID', serialize=False, primary_key=True)),
                ('name', models.TextField(help_text=b'Name of character')),
                ('dob', models.DateTimeField(default=datetime.datetime(2015, 8, 5, 9, 9, 9, 394158), help_text=b'DoB of character')),
                ('race', models.TextField(default=b'', help_text=b'Race of character')),
                ('bloodline', models.TextField(default=b'', help_text=b'Bloodline of character')),
                ('ancestry', models.TextField(default=b'', help_text=b'Ancestry of character')),
                ('gender', models.TextField(default=b'Male', help_text=b'Gender')),
                ('corp_name', models.TextField(default=b'', help_text=b'Name of corporation character is member of')),
                ('corp_id', models.BigIntegerField(default=0, help_text=b'id of corporation')),
                ('alliance_name', models.TextField(default=b'', help_text=b'Name of alliance')),
                ('alliance_id', models.BigIntegerField(default=0, help_text=b'id of alliance')),
                ('clone_name', models.TextField(default=b'', help_text=b'clone level name')),
                ('clone_skill_points', models.PositiveIntegerField(default=0, help_text=b'max SP of clone')),
                ('balance', models.BigIntegerField(default=0, help_text=b'isk on hand')),
                ('implant_memory_name', models.TextField(default=b'', help_text=b'name of memory implant')),
                ('implant_memory_bonus', models.PositiveIntegerField(default=0, help_text=b'memory bonus')),
                ('implant_intelligence_name', models.TextField(default=b'', help_text=b'name of intelligence implant')),
                ('implant_intelligence_bonus', models.PositiveIntegerField(default=0, help_text=b'intelligence bonus')),
                ('implant_charisma_name', models.TextField(default=b'', help_text=b'name of charisma implant')),
                ('implant_charisma_bonus', models.PositiveIntegerField(default=0, help_text=b'charisma bonus')),
                ('implant_willpower_name', models.TextField(default=b'', help_text=b'name of willpower implant')),
                ('implant_willpower_bonus', models.PositiveIntegerField(default=0, help_text=b'willpower bonus')),
                ('implant_perception_name', models.TextField(default=b'', help_text=b'name of perception implant')),
                ('implant_perception_bonus', models.PositiveIntegerField(default=0, help_text=b'perception bonus')),
                ('cached_until', models.DateTimeField(default=datetime.datetime(2015, 8, 5, 9, 9, 9, 394582), help_text=b'data cached until')),
            ],
            options={
                'verbose_name': 'Character',
                'verbose_name_plural': 'Characters',
            },
        ),
        migrations.CreateModel(
            name='CharSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skillpoints', models.PositiveIntegerField(help_text=b'SP trained')),
                ('level', models.PositiveIntegerField(help_text=b'level trained')),
            ],
        ),
        migrations.CreateModel(
            name='Corp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('corp_id', models.BigIntegerField(help_text=b'Corporation ID', db_index=True)),
                ('name', models.TextField(help_text=b'Corporation name')),
                ('ticker', models.TextField(help_text=b'Corp ticker')),
                ('ceo_id', models.BigIntegerField(help_text=b'character ID of CEO')),
                ('ceo_name', models.TextField(help_text=b'CEO Name')),
                ('description', models.TextField(help_text=b'Description of corp if provided')),
                ('url', models.TextField(help_text=b'URL for corporation')),
                ('tax_rate', models.PositiveIntegerField(help_text=b'Tax rate of corporation')),
                ('member_count', models.PositiveIntegerField(help_text=b'Number of members of corp')),
                ('member_limit', models.PositiveIntegerField(help_text=b'Max number of members corp can support')),
                ('shares', models.PositiveIntegerField(help_text=b'Number of shares of corp outstanding')),
            ],
            options={
                'verbose_name': 'Corporation',
                'verbose_name_plural': 'Corporations',
            },
        ),
        migrations.CreateModel(
            name='CorpDivision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_key', models.PositiveIntegerField(help_text=b'account key of corporation division')),
                ('description', models.TextField(help_text=b'Name of division')),
            ],
        ),
        migrations.CreateModel(
            name='CorpPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view_wallet', models.BooleanField(help_text=b'can view corporate wallet')),
                ('view_transaction', models.BooleanField(help_text=b'can view corporate transactions')),
                ('view_research', models.BooleanField(help_text=b'can view corporate research')),
                ('modify_rights', models.BooleanField(help_text=b'can modify corprate rights')),
            ],
        ),
        migrations.CreateModel(
            name='CorpWalletDivision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_key', models.PositiveIntegerField(help_text=b'account key of corporation wallet account division')),
                ('description', models.TextField(help_text=b'Name of wallet account division')),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref_id', models.BigIntegerField(help_text=b"Unique refID from CCP for this journal entry. Not primary key - multiple characters could have access to a single corporation's wallet API.")),
                ('date', models.DateTimeField(help_text=b'Date and time of the transaction.')),
                ('amount', models.FloatField(help_text=b'Amount transferred between parties.')),
                ('balance', models.FloatField(help_text=b'Balance in this wallet after this transaction.')),
                ('owner_name_1', models.TextField(help_text=b'Name of first party in the transaction.')),
                ('owner_id_1', models.BigIntegerField(help_text=b'Character or corporation ID of the first party.')),
                ('owner_name_2', models.TextField(help_text=b'Name of second party in the transaction.')),
                ('owner_id_2', models.BigIntegerField(help_text=b'Character or corporation ID of the second party.')),
                ('arg_name_1', models.TextField(help_text=b'Has different meanings - see: http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML#Arguments')),
                ('arg_id_1', models.PositiveIntegerField(help_text=b'Has different meanings - see: http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML#Arguments')),
                ('reason', models.TextField(help_text=b'Has different meanings - see: http://wiki.eve-id.net/APIv2_Char_JournalEntries_XML#Arguments')),
                ('tax_receiver_id', models.BigIntegerField(help_text=b'CorpID who received tax for this transaction.')),
                ('tax_amount', models.FloatField(help_text=b'Amount of tax for this transaction.')),
            ],
            options={
                'verbose_name': 'Journal Entry',
                'verbose_name_plural': 'Journal Entries',
            },
        ),
    ]
