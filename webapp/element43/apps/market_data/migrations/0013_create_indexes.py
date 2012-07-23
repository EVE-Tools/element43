# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute('CREATE INDEX market_data_orders_typeid_regionid ON market_data_orders (type_id, region_id)')
        db.execute('CREATE INDEX market_data_orderswarehouse_typeid_regionid ON market_data_orderswarehouse (type_id, region_id)')
        db.execute('CREATE INDEX market_data_history_typeid_regionid ON market_data_history (type_id, region_id)')
        db.execute('CREATE INDEX market_data_orders_typeid_stationid_isbid ON market_data_orders (type_id, station_id, is_bid)')

    def backwards(self, orm):
        db.execute('DROP INDEX market_data_orders_typeid_regionid')
        db.execute('DROP INDEX market_data_orderswarehouse_typeid_regionid')
        db.execute('DROP INDEX market_data_history_typeid_regionid')
        db.execute('DROP INDEX market_data_orders_typeid_stationid_isbid')

    models = {
        'market_data.emdrstats': {
            'Meta': {'object_name': 'EmdrStats'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
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
            'region_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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
            'type_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
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
            'type_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
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