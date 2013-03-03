# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RamuraDeVarsta'
        db.create_table('structuri_ramuradevarsta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('varsta_intrare', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('varsta_iesire', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('structuri', ['RamuraDeVarsta'])

        # Adding model 'CentruLocal'
        db.create_table('structuri_centrulocal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data_infiintare', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('localitate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('denumire', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('specific', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('structuri', ['CentruLocal'])

        # Adding model 'Unitate'
        db.create_table('structuri_unitate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data_infiintare', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ramura_de_varsta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structuri.RamuraDeVarsta'])),
            ('centru_local', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structuri.CentruLocal'])),
        ))
        db.send_create_signal('structuri', ['Unitate'])

        # Adding model 'Patrula'
        db.create_table('structuri_patrula', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data_infiintare', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('unitate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structuri.Unitate'])),
        ))
        db.send_create_signal('structuri', ['Patrula'])

        # Adding model 'Utilizator'
        db.create_table('structuri_utilizator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('prenume', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('structuri', ['Utilizator'])

        # Adding model 'Membru'
        db.create_table('structuri_membru', (
            ('utilizator_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['structuri.Utilizator'], unique=True, primary_key=True)),
            ('cnp', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('structuri', ['Membru'])

        # Adding model 'TipAsociereMembruStructura'
        db.create_table('structuri_tipasocieremembrustructura', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('structuri', ['TipAsociereMembruStructura'])

        # Adding model 'AsociereMembruStructura'
        db.create_table('structuri_asocieremembrustructura', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membru', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structuri.Membru'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tip_asociere', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structuri.TipAsociereMembruStructura'])),
            ('moment_inceput', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('moment_incheiere', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('structuri', ['AsociereMembruStructura'])


    def backwards(self, orm):
        
        # Deleting model 'RamuraDeVarsta'
        db.delete_table('structuri_ramuradevarsta')

        # Deleting model 'CentruLocal'
        db.delete_table('structuri_centrulocal')

        # Deleting model 'Unitate'
        db.delete_table('structuri_unitate')

        # Deleting model 'Patrula'
        db.delete_table('structuri_patrula')

        # Deleting model 'Utilizator'
        db.delete_table('structuri_utilizator')

        # Deleting model 'Membru'
        db.delete_table('structuri_membru')

        # Deleting model 'TipAsociereMembruStructura'
        db.delete_table('structuri_tipasocieremembrustructura')

        # Deleting model 'AsociereMembruStructura'
        db.delete_table('structuri_asocieremembrustructura')


    models = {
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
        },
        'structuri.asocieremembrustructura': {
            'Meta': {'object_name': 'AsociereMembruStructura'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']"}),
            'moment_inceput': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'moment_incheiere': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tip_asociere': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TipAsociereMembruStructura']"})
        },
        'structuri.centrulocal': {
            'Meta': {'object_name': 'CentruLocal'},
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'denumire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localitate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'specific': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'structuri.membru': {
            'Meta': {'object_name': 'Membru', '_ormbases': ['structuri.Utilizator']},
            'cnp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'utilizator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['structuri.Utilizator']", 'unique': 'True', 'primary_key': 'True'})
        },
        'structuri.patrula': {
            'Meta': {'object_name': 'Patrula'},
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unitate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Unitate']"})
        },
        'structuri.ramuradevarsta': {
            'Meta': {'object_name': 'RamuraDeVarsta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'varsta_iesire': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'varsta_intrare': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'structuri.tipasocieremembrustructura': {
            'Meta': {'object_name': 'TipAsociereMembruStructura'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'structuri.unitate': {
            'Meta': {'object_name': 'Unitate'},
            'centru_local': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.CentruLocal']"}),
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ramura_de_varsta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.RamuraDeVarsta']"})
        },
        'structuri.utilizator': {
            'Meta': {'object_name': 'Utilizator'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['structuri']
