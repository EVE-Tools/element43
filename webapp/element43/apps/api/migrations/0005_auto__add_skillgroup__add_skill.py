# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SkillGroup'
        db.create_table('api_skillgroup', (
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('api', ['SkillGroup'])

        # Adding model 'Skill'
        db.create_table('api_skill', (
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.SkillGroup'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('primary_attribute', self.gf('django.db.models.fields.TextField')()),
            ('secondary_attribute', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('api', ['Skill'])


    def backwards(self, orm):
        # Deleting model 'SkillGroup'
        db.delete_table('api_skillgroup')

        # Deleting model 'Skill'
        db.delete_table('api_skill')


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
            'alliance_id': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'alliance_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'ancestry': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.APIKey']"}),
            'balance': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'bloodline': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'cached_until': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 5, 0, 0)'}),
            'clone_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'clone_skill_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'corp_id': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'corp_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dob': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 5, 0, 0)'}),
            'gender': ('django.db.models.fields.TextField', [], {'default': "'Male'"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'implant_charisma_bonus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'implant_charisma_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'implant_intelligence_bonus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'implant_intelligence_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'implant_memory_bonus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'implant_memory_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'implant_perception_bonus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'implant_perception_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'implant_willpower_bonus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'implant_willpower_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'race': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
        'api.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.SkillGroup']"}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'primary_attribute': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secondary_attribute': ('django.db.models.fields.TextField', [], {})
        },
        'api.skillgroup': {
            'Meta': {'object_name': 'SkillGroup'},
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
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