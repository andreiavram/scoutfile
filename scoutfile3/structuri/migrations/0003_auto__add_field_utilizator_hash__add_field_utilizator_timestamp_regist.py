# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Utilizator.hash'
        db.add_column('structuri_utilizator', 'hash', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True), keep_default=False)

        # Adding field 'Utilizator.timestamp_registered'
        db.add_column('structuri_utilizator', 'timestamp_registered', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Utilizator.timestamp_confirmed'
        db.add_column('structuri_utilizator', 'timestamp_confirmed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Utilizator.timestamp_accepted'
        db.add_column('structuri_utilizator', 'timestamp_accepted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding unique constraint on 'Utilizator', fields ['email']
        db.create_unique('structuri_utilizator', ['email'])

        # Adding unique constraint on 'Membru', fields ['cnp']
        db.create_unique('structuri_membru', ['cnp'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Membru', fields ['cnp']
        db.delete_unique('structuri_membru', ['cnp'])

        # Removing unique constraint on 'Utilizator', fields ['email']
        db.delete_unique('structuri_utilizator', ['email'])

        # Deleting field 'Utilizator.hash'
        db.delete_column('structuri_utilizator', 'hash')

        # Deleting field 'Utilizator.timestamp_registered'
        db.delete_column('structuri_utilizator', 'timestamp_registered')

        # Deleting field 'Utilizator.timestamp_confirmed'
        db.delete_column('structuri_utilizator', 'timestamp_confirmed')

        # Deleting field 'Utilizator.timestamp_accepted'
        db.delete_column('structuri_utilizator', 'timestamp_accepted')


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
            'adresa': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'cnp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'telefon': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
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
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp_confirmed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp_registered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['structuri']
