# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eve_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedOrders',
            fields=[
                ('generated_at', models.DateTimeField(help_text=b"When the market data was generated on the user's machine.", null=True, blank=True)),
                ('price', models.FloatField(help_text=b'Item price, as reported in the message.')),
                ('volume_remaining', models.PositiveIntegerField(help_text=b'Number of remaining items for sale.')),
                ('volume_entered', models.PositiveIntegerField(help_text=b'Number of items initially put up for sale.')),
                ('minimum_volume', models.PositiveIntegerField(help_text=b'Minimum volume before the order finishes.')),
                ('order_range', models.IntegerField(help_text=b'How far the order is visible.  32767 = region-wide')),
                ('id', models.BigIntegerField(help_text=b'Unique order ID from EVE for this order.', serialize=False, primary_key=True)),
                ('is_bid', models.BooleanField(help_text=b'If True, this is a buy order. If False, this is a sell order.')),
                ('issue_date', models.DateTimeField(help_text=b'When the order was issued.')),
                ('duration', models.PositiveSmallIntegerField(help_text=b'The duration of the order, in days.')),
                ('is_suspicious', models.BooleanField(help_text=b"If this is True, we have reason to question this order's validity")),
                ('message_key', models.CharField(help_text=b'The unique hash that of the market message.', max_length=255, null=True, blank=True)),
                ('uploader_ip_hash', models.CharField(help_text=b'The unique hash for the person who uploaded this message.', max_length=255)),
                ('is_active', models.BooleanField(default=True, help_text=b'is this a live order or is it history')),
                ('invtype', models.ForeignKey(help_text=b'The Type ID of the item in the order.', to='eve_db.InvType')),
                ('mapregion', models.ForeignKey(help_text=b'Region ID the order originated from.', to='eve_db.MapRegion')),
                ('mapsolarsystem', models.ForeignKey(help_text=b'ID of the solar system the order is in.', to='eve_db.MapSolarSystem')),
                ('stastation', models.ForeignKey(help_text=b'The station that this order is in.', to='eve_db.StaStation')),
            ],
            options={
                'verbose_name': 'Archived Market Order',
                'verbose_name_plural': 'Archived Market Orders',
            },
        ),
        migrations.CreateModel(
            name='EmdrStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_type', models.SmallIntegerField(help_text=b'Message type for statistics')),
                ('status_count', models.PositiveIntegerField(help_text=b'Count of messages of specific type')),
                ('message_timestamp', models.DateTimeField(help_text=b'When the stats were counted for this entry', auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'Message Statistics Data',
                'verbose_name_plural': 'Message Statistics Data',
            },
        ),
        migrations.CreateModel(
            name='EmdrStatsWorking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_type', models.SmallIntegerField(help_text=b'Message type for statistics')),
            ],
            options={
                'verbose_name': 'Message Statistics Live Data',
                'verbose_name_plural': 'Message Statistics Live Data',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.CharField(help_text=b'Primary key, based on UUID', max_length=255, serialize=False, primary_key=True)),
                ('history_data', models.TextField(help_text=b'Compressed zlib data of the JSON message for history')),
                ('invtype', models.ForeignKey(help_text=b'The Type ID of the item in the order.', to='eve_db.InvType')),
                ('mapregion', models.ForeignKey(help_text=b'Region ID the order originated from.', to='eve_db.MapRegion')),
            ],
            options={
                'verbose_name': 'History Data',
                'verbose_name_plural': 'History Data',
            },
        ),
        migrations.CreateModel(
            name='ItemRegionStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buymean', models.FloatField(help_text=b'Mean of buy price')),
                ('buyavg', models.FloatField(help_text=b'Average of buy price')),
                ('sellmean', models.FloatField(help_text=b'Mean of sell price')),
                ('sellavg', models.FloatField(help_text=b'Avg of sell price')),
                ('buymedian', models.FloatField(help_text=b'Median of buy price')),
                ('sellmedian', models.FloatField(help_text=b'Median of sell price')),
                ('buyvolume', models.BigIntegerField(help_text=b'total volume traded')),
                ('sellvolume', models.BigIntegerField(help_text=b'total volume traded')),
                ('buy_95_percentile', models.FloatField(help_text=b'95th % of buy orders')),
                ('sell_95_percentile', models.FloatField(help_text=b'95th % of sell orders')),
                ('buy_std_dev', models.FloatField(help_text=b'standard deviation of buy orders')),
                ('sell_std_dev', models.FloatField(help_text=b'standard deviation of sell orders')),
                ('lastupdate', models.DateTimeField(help_text=b'Date the stats were updated', null=True, blank=True)),
                ('invtype', models.ForeignKey(help_text=b'FK to type table', to='eve_db.InvType')),
                ('mapregion', models.ForeignKey(help_text=b'FK to region table', to='eve_db.MapRegion')),
            ],
            options={
                'verbose_name': 'Stat Data',
                'verbose_name_plural': 'Stats Data',
            },
        ),
        migrations.CreateModel(
            name='ItemRegionStatHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buymean', models.FloatField(help_text=b'Mean of buy price')),
                ('buyavg', models.FloatField(help_text=b'Average of buy price')),
                ('sellmean', models.FloatField(help_text=b'Mean of sell price')),
                ('sellavg', models.FloatField(help_text=b'Avg of sell price')),
                ('buymedian', models.FloatField(help_text=b'Median of buy price')),
                ('sellmedian', models.FloatField(help_text=b'Median of sell price')),
                ('buyvolume', models.BigIntegerField(help_text=b'total volume traded')),
                ('sellvolume', models.BigIntegerField(help_text=b'total volume traded')),
                ('buy_95_percentile', models.FloatField(help_text=b'95th % of buy orders')),
                ('sell_95_percentile', models.FloatField(help_text=b'95th % of sell orders')),
                ('buy_std_dev', models.FloatField(help_text=b'standard deviation of buy orders')),
                ('sell_std_dev', models.FloatField(help_text=b'standard deviation of sell orders')),
                ('date', models.DateTimeField(help_text=b'Date the stats were inserted', null=True, blank=True)),
                ('invtype', models.ForeignKey(help_text=b'FK to type table', to='eve_db.InvType')),
                ('mapregion', models.ForeignKey(help_text=b'FK to region table', to='eve_db.MapRegion')),
            ],
            options={
                'verbose_name': 'Stat History Data',
                'verbose_name_plural': 'Stat History Data',
            },
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(help_text=b'Date of the data')),
                ('numorders', models.PositiveIntegerField(help_text=b'number of transactions for this item/region')),
                ('low', models.FloatField(help_text=b'low price of orders for this item/region')),
                ('high', models.FloatField(help_text=b'high price of orders for this item/region')),
                ('mean', models.FloatField(help_text=b'mean price of orders for this item/region')),
                ('quantity', models.BigIntegerField(help_text=b'quantity of item sold for this item/region')),
                ('invtype', models.ForeignKey(help_text=b'The Type ID of the item in the order.', to='eve_db.InvType')),
                ('mapregion', models.ForeignKey(help_text=b'Region ID the order originated from.', to='eve_db.MapRegion')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('generated_at', models.DateTimeField(help_text=b"When the market data was generated on the user's machine.", null=True, blank=True)),
                ('price', models.FloatField(help_text=b'Item price, as reported in the message.')),
                ('volume_remaining', models.PositiveIntegerField(help_text=b'Number of remaining items for sale.')),
                ('volume_entered', models.PositiveIntegerField(help_text=b'Number of items initially put up for sale.')),
                ('minimum_volume', models.PositiveIntegerField(help_text=b'Minimum volume before the order finishes.')),
                ('order_range', models.IntegerField(help_text=b'How far the order is visible.  32767 = region-wide')),
                ('id', models.BigIntegerField(help_text=b'Unique order ID from EVE for this order.', serialize=False, primary_key=True)),
                ('is_bid', models.BooleanField(help_text=b'If True, this is a buy order. If False, this is a sell order.')),
                ('issue_date', models.DateTimeField(help_text=b'When the order was issued.')),
                ('duration', models.PositiveSmallIntegerField(help_text=b'The duration of the order, in days.')),
                ('is_suspicious', models.BooleanField(help_text=b"If this is True, we have reason to question this order's validity")),
                ('message_key', models.CharField(help_text=b'The unique hash that of the market message.', max_length=255, null=True, blank=True)),
                ('uploader_ip_hash', models.CharField(help_text=b'The unique hash for the person who uploaded this message.', max_length=255)),
                ('is_active', models.BooleanField(default=True, help_text=b'is this a live order or is it history')),
                ('invtype', models.ForeignKey(help_text=b'The Type ID of the item in the order.', to='eve_db.InvType')),
                ('mapregion', models.ForeignKey(help_text=b'Region ID the order originated from.', to='eve_db.MapRegion')),
                ('mapsolarsystem', models.ForeignKey(help_text=b'ID of the solar system the order is in.', to='eve_db.MapSolarSystem')),
                ('stastation', models.ForeignKey(help_text=b'The station that this order is in.', to='eve_db.StaStation')),
            ],
            options={
                'verbose_name': 'Market Order',
                'verbose_name_plural': 'Market Orders',
            },
        ),
        migrations.CreateModel(
            name='SeenOrders',
            fields=[
                ('id', models.BigIntegerField(help_text=b'Order ID', serialize=False, primary_key=True)),
                ('region_id', models.PositiveIntegerField(help_text=b'Region ID of seen order')),
                ('type_id', models.PositiveIntegerField(help_text=b'Type ID of seen order')),
            ],
            options={
                'verbose_name': 'Seen Order',
                'verbose_name_plural': 'Seen Orders',
            },
        ),
        migrations.CreateModel(
            name='UUDIFMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b"I'm assuming this is a unique hash for the message.", unique=True, max_length=255)),
                ('received_dtime', models.DateTimeField(help_text=b'Time of initial receiving.', auto_now_add=True)),
                ('is_order', models.BooleanField(help_text=b'If True, this is an order. If False, this is history.')),
                ('message', models.TextField(help_text=b'Full JSON representation of the message.')),
            ],
            options={
                'verbose_name': 'UUDIF Message',
                'verbose_name_plural': 'UUDIF Messages',
            },
        ),
    ]
