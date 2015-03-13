# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CodPostal'
        db.create_table('adrese_postale_codpostal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cod_postal', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('judet', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('localitate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tip_strada', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('strada', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('adrese_postale', ['CodPostal'])


    def backwards(self, orm):
        # Deleting model 'CodPostal'
        db.delete_table('adrese_postale_codpostal')


    models = {
        'adrese_postale.codpostal': {
            'Meta': {'object_name': 'CodPostal'},
            'cod_postal': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judet': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'localitate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sector': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'strada': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tip_strada': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['adrese_postale']