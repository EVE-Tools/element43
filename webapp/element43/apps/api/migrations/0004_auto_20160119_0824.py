# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_system_check_fixes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charskill',
            options={'verbose_name': 'Character Skill', 'verbose_name_plural': 'Character Skills'},
        ),
        migrations.AlterModelOptions(
            name='corpdivision',
            options={'verbose_name': 'Corporation Division', 'verbose_name_plural': 'Corporation Divisions'},
        ),
        migrations.RemoveField(
            model_name='corp',
            name='id',
        ),
        migrations.AlterField(
            model_name='corp',
            name='corp_id',
            field=models.BigIntegerField(help_text=b'Corporation ID', serialize=False, primary_key=True),
        ),
        migrations.AlterUniqueTogether(
            name='apikey',
            unique_together=set([('user', 'keyid')]),
        ),
        migrations.AlterUniqueTogether(
            name='apitimer',
            unique_together=set([('character', 'corporation', 'apisheet')]),
        ),
        migrations.AlterUniqueTogether(
            name='charskill',
            unique_together=set([('character', 'skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='journalentry',
            unique_together=set([('ref_id', 'character')]),
        ),
        migrations.AlterUniqueTogether(
            name='markettransaction',
            unique_together=set([('journal_transaction_id', 'character', 'corporation')]),
        ),
    ]
