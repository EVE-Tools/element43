# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CharSkill'
        db.create_table('api_charskill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Character'])),
            ('skill_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('skillpoints', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('api', ['CharSkill'])

        # Adding field 'Character.birthday'
        db.add_column('api_character', 'birthday',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Character.race'
        db.add_column('api_character', 'race',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.bloodline'
        db.add_column('api_character', 'bloodline',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.ancestry'
        db.add_column('api_character', 'ancestry',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.gender'
        db.add_column('api_character', 'gender',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.corp_name'
        db.add_column('api_character', 'corp_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.corp_id'
        db.add_column('api_character', 'corp_id',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Character.alliance_name'
        db.add_column('api_character', 'alliance_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.alliance_id'
        db.add_column('api_character', 'alliance_id',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.clone_name'
        db.add_column('api_character', 'clone_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.clone_skill_points'
        db.add_column('api_character', 'clone_skill_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.balance'
        db.add_column('api_character', 'balance',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.implant_memory_name'
        db.add_column('api_character', 'implant_memory_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.implant_memory_bonus'
        db.add_column('api_character', 'implant_memory_bonus',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.implant_intelligence_name'
        db.add_column('api_character', 'implant_intelligence_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.implant_intelligence_bonus'
        db.add_column('api_character', 'implant_intelligence_bonus',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.implant_charisma_name'
        db.add_column('api_character', 'implant_charisma_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.implant_charisma_bonus'
        db.add_column('api_character', 'implant_charisma_bonus',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.implant_willpower_name'
        db.add_column('api_character', 'implant_willpower_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.implant_willpower_bonus'
        db.add_column('api_character', 'implant_willpower_bonus',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.implant_perception_name'
        db.add_column('api_character', 'implant_perception_name',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Character.implant_perception_bonus'
        db.add_column('api_character', 'implant_perception_bonus',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.cached_until'
        db.add_column('api_character', 'cached_until',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'CharSkill'
        db.delete_table('api_charskill')

        # Deleting field 'Character.birthday'
        db.delete_column('api_character', 'birthday')

        # Deleting field 'Character.race'
        db.delete_column('api_character', 'race')

        # Deleting field 'Character.bloodline'
        db.delete_column('api_character', 'bloodline')

        # Deleting field 'Character.ancestry'
        db.delete_column('api_character', 'ancestry')

        # Deleting field 'Character.gender'
        db.delete_column('api_character', 'gender')

        # Deleting field 'Character.corp_name'
        db.delete_column('api_character', 'corp_name')

        # Deleting field 'Character.corp_id'
        db.delete_column('api_character', 'corp_id')

        # Deleting field 'Character.alliance_name'
        db.delete_column('api_character', 'alliance_name')

        # Deleting field 'Character.alliance_id'
        db.delete_column('api_character', 'alliance_id')

        # Deleting field 'Character.clone_name'
        db.delete_column('api_character', 'clone_name')

        # Deleting field 'Character.clone_skill_points'
        db.delete_column('api_character', 'clone_skill_points')

        # Deleting field 'Character.balance'
        db.delete_column('api_character', 'balance')

        # Deleting field 'Character.implant_memory_name'
        db.delete_column('api_character', 'implant_memory_name')

        # Deleting field 'Character.implant_memory_bonus'
        db.delete_column('api_character', 'implant_memory_bonus')

        # Deleting field 'Character.implant_intelligence_name'
        db.delete_column('api_character', 'implant_intelligence_name')

        # Deleting field 'Character.implant_intelligence_bonus'
        db.delete_column('api_character', 'implant_intelligence_bonus')

        # Deleting field 'Character.implant_charisma_name'
        db.delete_column('api_character', 'implant_charisma_name')

        # Deleting field 'Character.implant_charisma_bonus'
        db.delete_column('api_character', 'implant_charisma_bonus')

        # Deleting field 'Character.implant_willpower_name'
        db.delete_column('api_character', 'implant_willpower_name')

        # Deleting field 'Character.implant_willpower_bonus'
        db.delete_column('api_character', 'implant_willpower_bonus')

        # Deleting field 'Character.implant_perception_name'
        db.delete_column('api_character', 'implant_perception_name')

        # Deleting field 'Character.implant_perception_bonus'
        db.delete_column('api_character', 'implant_perception_bonus')

        # Deleting field 'Character.cached_until'
        db.delete_column('api_character', 'cached_until')


    models = {
        'api.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'accessmask': ('django.db.models.fields.BigIntegerField', [], {}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keyid': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vcode': ('django.db.models.fields.TextField', [], {})
        },
        'api.apitimer': {
            'Meta': {'object_name': 'APITimer'},
            'apisheet': ('django.db.models.fields.TextField', [], {}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nextupdate': ('django.db.models.fields.DateTimeField', [], {})
        },
        'api.character': {
            'Meta': {'object_name': 'Character'},
            'alliance_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'alliance_name': ('django.db.models.fields.TextField', [], {}),
            'ancestry': ('django.db.models.fields.TextField', [], {}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.APIKey']"}),
            'balance': ('django.db.models.fields.BigIntegerField', [], {}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'bloodline': ('django.db.models.fields.TextField', [], {}),
            'cached_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'clone_name': ('django.db.models.fields.TextField', [], {}),
            'clone_skill_points': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'corp_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'corp_name': ('django.db.models.fields.TextField', [], {}),
            'gender': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'implant_charisma_bonus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_charisma_name': ('django.db.models.fields.TextField', [], {}),
            'implant_intelligence_bonus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_intelligence_name': ('django.db.models.fields.TextField', [], {}),
            'implant_memory_bonus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_memory_name': ('django.db.models.fields.TextField', [], {}),
            'implant_perception_bonus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_perception_name': ('django.db.models.fields.TextField', [], {}),
            'implant_willpower_bonus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_willpower_name': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'race': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.charskill': {
            'Meta': {'object_name': 'CharSkill'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'skill_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'skillpoints': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']