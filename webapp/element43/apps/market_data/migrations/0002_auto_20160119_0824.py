# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderhistory',
            options={'verbose_name': 'Uncompressed History Data', 'verbose_name_plural': 'Uncompressed History Data'},
        ),
        migrations.AlterUniqueTogether(
            name='itemregionstat',
            unique_together=set([('mapregion', 'invtype')]),
        ),
        migrations.AlterUniqueTogether(
            name='itemregionstathistory',
            unique_together=set([('mapregion', 'invtype', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='orderhistory',
            unique_together=set([('mapregion', 'invtype', 'date')]),
        ),
        migrations.AlterIndexTogether(
            name='orders',
            index_together=set([('mapregion', 'invtype', 'is_active')]),
        ),
    ]
