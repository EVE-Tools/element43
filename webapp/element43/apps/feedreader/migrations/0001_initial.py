# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'Newsfeed URL')),
                ('name', models.CharField(help_text=b'Name of the feed', max_length=100)),
                ('icon_file', models.CharField(help_text=b"Name of the feed's icon file", max_length=100)),
                ('next_update', models.DateTimeField(help_text=b'Timestamp for next update')),
            ],
            options={
                'verbose_name': 'Newsfeed',
                'verbose_name_plural': 'Newsfeeds',
            },
        ),
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Title of the item', max_length=100)),
                ('description', models.TextField(help_text=b'Short description of the item')),
                ('link', models.URLField(help_text=b'Link to the text')),
                ('published', models.DateTimeField(help_text=b'Time the item was published')),
                ('feed', models.ForeignKey(help_text=b'FKey relationship to feed table', to='feedreader.Feed')),
            ],
            options={
                'verbose_name': 'Feed Item',
                'verbose_name_plural': 'Feed Items',
            },
        ),
    ]
