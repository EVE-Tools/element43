# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SeenOrdersWorking'
        db.delete_table('market_data_seenordersworking')

        # Adding model 'OrdersWarehouse'
        db.create_table('market_data_orderswarehouse', (
            ('generated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('region_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('volume_entered', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order_range', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('is_bid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('issue_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('station_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('solar_system_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_suspicious', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('message_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uploader_ip_hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('market_data', ['OrdersWarehouse'])


    def backwards(self, orm):
        # Adding model 'SeenOrdersWorking'
        db.create_table('market_data_seenordersworking', (
            ('type_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('region_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('market_data', ['SeenOrdersWorking'])

        # Deleting model 'OrdersWarehouse'
        db.delete_table('market_data_orderswarehouse')


    models = {
        'market_data.emdrstats': {
            'Meta': {'object_name': 'EmdrStats'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status_type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'market_data.emdrstatsworking': {
            'Meta': {'object_name': 'EmdrStatsWorking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'market_data.history': {
            'Meta': {'object_name': 'History'},
            'history_data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'region_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'market_data.orders': {
            'Meta': {'object_name': 'Orders'},
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'generated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_bid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suspicious': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {}),
            'message_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'minimum_volume': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order_range': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'region_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'solar_system_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'station_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'uploader_ip_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume_entered': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'volume_remaining': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'market_data.orderswarehouse': {
            'Meta': {'object_name': 'OrdersWarehouse'},
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'generated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_bid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suspicious': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {}),
            'message_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_range': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'region_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'solar_system_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'station_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'uploader_ip_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume_entered': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'market_data.seenorders': {
            'Meta': {'object_name': 'SeenOrders'},
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'region_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'market_data.uudifmessage': {
            'Meta': {'object_name': 'UUDIFMessage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'received_dtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['market_data']