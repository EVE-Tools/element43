# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OrdersWarehouse'
        db.delete_table('market_data_orderswarehouse')

        # Adding field 'ItemRegionStatHistory.buy_std_dev'
        db.add_column('market_data_itemregionstathistory', 'buy_std_dev',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'ItemRegionStatHistory.sell_std_dev'
        db.add_column('market_data_itemregionstathistory', 'sell_std_dev',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'OrdersWarehouse'
        db.create_table('market_data_orderswarehouse', (
            ('stastation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_db.StaStation'])),
            ('issue_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_bid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_db.InvType'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('is_suspicious', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mapsolarsystem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_db.MapSolarSystem'])),
            ('order_range', self.gf('django.db.models.fields.IntegerField')()),
            ('message_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('volume_entered', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('uploader_ip_hash', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('duration', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('generated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('mapregion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve_db.MapRegion'])),
        ))
        db.send_create_signal('market_data', ['OrdersWarehouse'])

        # Deleting field 'ItemRegionStatHistory.buy_std_dev'
        db.delete_column('market_data_itemregionstathistory', 'buy_std_dev')

        # Deleting field 'ItemRegionStatHistory.sell_std_dev'
        db.delete_column('market_data_itemregionstathistory', 'sell_std_dev')


    models = {
        'eve_db.chrfaction': {
            'Meta': {'ordering': "['id']", 'object_name': 'ChrFaction'},
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faction_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'size_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solar_system': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faction_set'", 'null': 'True', 'to': "orm['eve_db.MapSolarSystem']"}),
            'station_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'station_system_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'eve_db.chrrace': {
            'Meta': {'ordering': "['id']", 'object_name': 'ChrRace'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'eve_db.crpnpccorporation': {
            'Meta': {'ordering': "['id']", 'object_name': 'CrpNPCCorporation'},
            'border_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'corridor_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enemy_corp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enemy_of_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'extent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrFaction']", 'null': 'True', 'blank': 'True'}),
            'friendly_corp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'friendly_with_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'fringe_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hub_systems': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'initial_share_price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested1_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor1_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested2_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor2_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested3_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor3_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'investor4': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invested4_set'", 'null': 'True', 'to': "orm['eve_db.CrpNPCCorporation']"}),
            'investor4_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_security': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public_share_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'size_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solar_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapSolarSystem']", 'null': 'True', 'blank': 'True'}),
            'station_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'station_system_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stations_are_scattered': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'eve_db.eveicon': {
            'Meta': {'ordering': "['id']", 'object_name': 'EveIcon'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'})
        },
        'eve_db.invcategory': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eve_db.invgroup': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvGroup'},
            'allow_anchoring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_manufacture': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_recycle': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_anchored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fittable_non_singleton': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'use_base_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'eve_db.invmarketgroup': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvMarketGroup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'has_items': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvMarketGroup']", 'null': 'True', 'blank': 'True'})
        },
        'eve_db.invtype': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvType'},
            'base_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'chance_of_duplicating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvGroup']", 'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.EveIcon']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'market_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvMarketGroup']", 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'portion_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrRace']", 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.mapconstellation': {
            'Meta': {'ordering': "['id']", 'object_name': 'MapConstellation'},
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrFaction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']", 'null': 'True', 'blank': 'True'}),
            'sovereignty_grace_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sovereignty_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.mapregion': {
            'Meta': {'ordering': "['id']", 'object_name': 'MapRegion'},
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.ChrFaction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.mapsolarsystem': {
            'Meta': {'ordering': "['id']", 'object_name': 'MapSolarSystem'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapConstellation']", 'null': 'True', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'solarsystem_set'", 'null': 'True', 'to': "orm['eve_db.ChrFaction']"}),
            'has_interconstellational_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_interregional_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_border_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_corridor_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fringe_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hub_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'luminosity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']", 'null': 'True', 'blank': 'True'}),
            'security_class': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'security_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sovereignty_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sovereignty_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']", 'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'x_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.staoperation': {
            'Meta': {'ordering': "['id']", 'object_name': 'StaOperation'},
            'activity_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amarr_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'amarr_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'border': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caldari_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'caldari_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'corridor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fringe': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gallente_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gallente_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'hub': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'jove_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'jove_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'minmatar_station_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'minmatar_station_operation_set'", 'null': 'True', 'to': "orm['eve_db.StaStationType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ratio': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.stastation': {
            'Meta': {'ordering': "['id']", 'object_name': 'StaStation'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapConstellation']", 'null': 'True', 'blank': 'True'}),
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.CrpNPCCorporation']", 'null': 'True', 'blank': 'True'}),
            'docking_cost_per_volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'max_ship_volume_dockable': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'office_rental_cost': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaOperation']", 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']", 'null': 'True', 'blank': 'True'}),
            'reprocessing_efficiency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reprocessing_hangar_flag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reprocessing_stations_take': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'security': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'solar_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapSolarSystem']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaStationType']", 'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'eve_db.stastationtype': {
            'Meta': {'ordering': "['id']", 'object_name': 'StaStationType'},
            'dock_entry_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_entry_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_entry_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_orientation_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_orientation_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dock_orientation_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_conquerable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'office_slots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaOperation']", 'null': 'True', 'blank': 'True'}),
            'reprocessing_efficiency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
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
            'invtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']"}),
            'mapregion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']"})
        },
        'market_data.itemregionstat': {
            'Meta': {'object_name': 'ItemRegionStat'},
            'buy_95_percentile': ('django.db.models.fields.FloatField', [], {}),
            'buyavg': ('django.db.models.fields.FloatField', [], {}),
            'buymean': ('django.db.models.fields.FloatField', [], {}),
            'buymedian': ('django.db.models.fields.FloatField', [], {}),
            'buyvolume': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']"}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mapregion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']"}),
            'sell_95_percentile': ('django.db.models.fields.FloatField', [], {}),
            'sellavg': ('django.db.models.fields.FloatField', [], {}),
            'sellmean': ('django.db.models.fields.FloatField', [], {}),
            'sellmedian': ('django.db.models.fields.FloatField', [], {}),
            'sellvolume': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'market_data.itemregionstathistory': {
            'Meta': {'object_name': 'ItemRegionStatHistory'},
            'buy_95_percentile': ('django.db.models.fields.FloatField', [], {}),
            'buy_std_dev': ('django.db.models.fields.FloatField', [], {}),
            'buyavg': ('django.db.models.fields.FloatField', [], {}),
            'buymean': ('django.db.models.fields.FloatField', [], {}),
            'buymedian': ('django.db.models.fields.FloatField', [], {}),
            'buyvolume': ('django.db.models.fields.BigIntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']"}),
            'mapregion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']"}),
            'sell_95_percentile': ('django.db.models.fields.FloatField', [], {}),
            'sell_std_dev': ('django.db.models.fields.FloatField', [], {}),
            'sellavg': ('django.db.models.fields.FloatField', [], {}),
            'sellmean': ('django.db.models.fields.FloatField', [], {}),
            'sellmedian': ('django.db.models.fields.FloatField', [], {}),
            'sellvolume': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'market_data.orderhistory': {
            'Meta': {'object_name': 'OrderHistory'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'high': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']"}),
            'low': ('django.db.models.fields.FloatField', [], {}),
            'mapregion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']"}),
            'mean': ('django.db.models.fields.FloatField', [], {}),
            'numorders': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'quantity': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'market_data.orders': {
            'Meta': {'object_name': 'Orders'},
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'generated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'invtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.InvType']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_bid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suspicious': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue_date': ('django.db.models.fields.DateTimeField', [], {}),
            'mapregion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapRegion']"}),
            'mapsolarsystem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.MapSolarSystem']"}),
            'message_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'minimum_volume': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order_range': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'stastation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_db.StaStation']"}),
            'uploader_ip_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'volume_entered': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'volume_remaining': ('django.db.models.fields.PositiveIntegerField', [], {})
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