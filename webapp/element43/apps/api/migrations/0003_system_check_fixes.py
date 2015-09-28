# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150805_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='cached_until',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text=b'data cached until'),
        ),
        migrations.AlterField(
            model_name='character',
            name='dob',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text=b'DoB of character'),
        ),
        migrations.AlterField(
            model_name='marketorder',
            name='id',
            field=models.OneToOneField(primary_key=True, serialize=False, to='market_data.Orders', help_text=b'Unique key for this order, uses CCP order ID'),
        ),
    ]
