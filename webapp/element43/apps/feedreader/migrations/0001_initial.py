# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table(u'feedreader_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('icon_file', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('next_update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'feedreader', ['Feed'])

        # Adding model 'FeedItem'
        db.create_table(u'feedreader_feeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedreader.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('published', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'feedreader', ['FeedItem'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table(u'feedreader_feed')

        # Deleting model 'FeedItem'
        db.delete_table(u'feedreader_feeditem')


    models = {
        u'feedreader.feed': {
            'Meta': {'object_name': 'Feed'},
            'icon_file': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'next_update': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'feedreader.feeditem': {
            'Meta': {'object_name': 'FeedItem'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feedreader.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['feedreader']