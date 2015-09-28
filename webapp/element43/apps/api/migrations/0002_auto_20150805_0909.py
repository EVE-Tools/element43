# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('market_data', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eve_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketOrder',
            fields=[
                ('id', models.ForeignKey(primary_key=True, serialize=False, to='market_data.Orders', help_text=b'Unique key for this order, uses CCP order ID')),
                ('order_state', models.PositiveIntegerField(help_text=b'Valid states: 0 = open/active, 1 = closed, 2 = expired (or fulfilled), 3 = cancelled, 4 = pending, 5 = character deleted')),
                ('account_key', models.PositiveIntegerField(help_text=b'Which division this order is using as its account. Always 1000 for characters, but in the range 1000 to 1006 for corporations.')),
                ('escrow', models.FloatField(help_text=b'Escrow amount for this order')),
                ('character', models.ForeignKey(default=None, to='api.Character', help_text=b'FK relationship to character table', null=True)),
                ('corporation', models.ForeignKey(default=None, to='api.Corp', help_text=b'FK relationship to corporation table', null=True)),
            ],
            options={
                'verbose_name': 'API Market Order',
                'verbose_name_plural': 'API Market Orders',
            },
        ),
        migrations.CreateModel(
            name='MarketTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(help_text=b'Date and time of the transaction.')),
                ('transaction_id', models.BigIntegerField(help_text=b'Non-unique transaction ID.')),
                ('quantity', models.IntegerField(help_text=b'Number of items bought/sold.')),
                ('price', models.FloatField(help_text=b'Price per unit of the item.')),
                ('client_id', models.BigIntegerField(help_text=b'Character or corporation ID of the other party.')),
                ('client_name', models.TextField(help_text=b'Name of other party.')),
                ('is_bid', models.BooleanField(help_text=b'Marks whether this item was bought or sold.')),
                ('is_corporate_transaction', models.BooleanField(help_text=b'Marks whether this is a corporate or a personal transaction.')),
                ('journal_transaction_id', models.BigIntegerField(help_text=b'Journal refID for this transaction.')),
                ('character', models.ForeignKey(default=None, to='api.Character', help_text=b'FK relationship to character table', null=True)),
                ('corporation', models.ForeignKey(default=None, to='api.Corp', help_text=b'FK relationship to corporation table', null=True)),
                ('invtype', models.ForeignKey(help_text=b'The item traded in this transaction.', to='eve_db.InvType')),
                ('station', models.ForeignKey(help_text=b'Station the transaction took place at.', to='eve_db.StaStation')),
            ],
            options={
                'verbose_name': 'Market Transaction',
                'verbose_name_plural': 'Market Transactions',
            },
        ),
        migrations.CreateModel(
            name='RefType',
            fields=[
                ('id', models.PositiveIntegerField(help_text=b'Unique refTypeID from API.', serialize=False, primary_key=True)),
                ('name', models.TextField(help_text=b'Name of this refType')),
            ],
            options={
                'verbose_name': 'API RefTypeID to name mapping',
                'verbose_name_plural': 'API RefTypeID to name mappings',
            },
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(help_text=b'The date the character began the current research with the agent at the current points per day.')),
                ('points_per_day', models.FloatField(help_text=b'The number of points generated per day.')),
                ('remainder_points', models.FloatField(help_text=b'The number of points remaining since last datacore purchase and/or points_per_day update.')),
                ('agent', models.ForeignKey(help_text=b'The agent.', to='eve_db.AgtAgent')),
                ('character', models.ForeignKey(help_text=b'Character who owns this job.', to='api.Character')),
            ],
            options={
                'verbose_name': 'Research Job',
                'verbose_name_plural': 'Research Jobs',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.PositiveIntegerField(help_text=b'Skill ID from API', serialize=False, primary_key=True)),
                ('name', models.TextField(help_text=b'Name of skill')),
                ('published', models.BooleanField(help_text=b'Published flag')),
                ('description', models.TextField(help_text=b'description of skill')),
                ('rank', models.PositiveIntegerField(help_text=b'skill difficulty rank')),
                ('primary_attribute', models.TextField(help_text=b'Primary attribute for skill')),
                ('secondary_attribute', models.TextField(help_text=b'secondary attribute for skill')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='SkillGroup',
            fields=[
                ('id', models.PositiveIntegerField(help_text=b'Group ID from API', serialize=False, primary_key=True)),
                ('name', models.TextField(help_text=b'Name of skill group')),
            ],
            options={
                'verbose_name': 'Skill Group',
                'verbose_name_plural': 'Skill Groups',
            },
        ),
        migrations.AddField(
            model_name='skill',
            name='group',
            field=models.ForeignKey(help_text=b'FK to skill group', to='api.SkillGroup'),
        ),
        migrations.AddField(
            model_name='research',
            name='skill',
            field=models.ForeignKey(help_text=b'The skill used for the research.', to='api.Skill'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='character',
            field=models.ForeignKey(default=None, to='api.Character', help_text=b'FK relationship to character table', null=True),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='corporation',
            field=models.ForeignKey(default=None, to='api.Corp', help_text=b'FK relationship to corporation table', null=True),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='ref_type',
            field=models.ForeignKey(help_text=b'Transaction type FKey relationship.', to='api.RefType'),
        ),
        migrations.AddField(
            model_name='corpwalletdivision',
            name='corporation',
            field=models.ForeignKey(help_text=b'FK to corporation table', to='api.Corp'),
        ),
        migrations.AddField(
            model_name='corppermissions',
            name='character',
            field=models.ForeignKey(help_text=b'FKey relationship to character table', to='api.Character'),
        ),
        migrations.AddField(
            model_name='corppermissions',
            name='corporation',
            field=models.ForeignKey(help_text=b'FK to corporation table', to='api.Corp'),
        ),
        migrations.AddField(
            model_name='corppermissions',
            name='user',
            field=models.ForeignKey(help_text=b'FKey relationship to user table', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='corpdivision',
            name='corporation',
            field=models.ForeignKey(help_text=b'FK to corporation table', to='api.Corp'),
        ),
        migrations.AddField(
            model_name='corp',
            name='stastation',
            field=models.ForeignKey(help_text=b'Station corp headquarters is in', to='eve_db.StaStation'),
        ),
        migrations.AddField(
            model_name='charskill',
            name='character',
            field=models.ForeignKey(help_text=b'FKey relationship to character table', to='api.Character'),
        ),
        migrations.AddField(
            model_name='charskill',
            name='skill',
            field=models.ForeignKey(help_text=b'FK relationship to skill table', to='api.Skill'),
        ),
        migrations.AddField(
            model_name='character',
            name='apikey',
            field=models.ForeignKey(help_text=b'FKey relationship to api key table', to='api.APIKey'),
        ),
        migrations.AddField(
            model_name='character',
            name='user',
            field=models.ForeignKey(help_text=b'FKey relationship to user table', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apitimer',
            name='character',
            field=models.ForeignKey(default=None, to='api.Character', help_text=b'FKey relationship to character table', null=True),
        ),
        migrations.AddField(
            model_name='apitimer',
            name='corporation',
            field=models.ForeignKey(default=None, to='api.Corp', help_text=b'FKey relationship to corporation table', null=True),
        ),
        migrations.AddField(
            model_name='apikey',
            name='user',
            field=models.ForeignKey(help_text=b'Fkey relationship to user table', to=settings.AUTH_USER_MODEL),
        ),
    ]
