# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CodPostal.descriptor'
        db.alter_column('adrese_postale_codpostal', 'descriptor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'CodPostal.descriptor'
        raise RuntimeError("Cannot reverse this migration. 'CodPostal.descriptor' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'CodPostal.descriptor'
        db.alter_column('adrese_postale_codpostal', 'descriptor', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'adrese_postale.codpostal': {
            'Meta': {'object_name': 'CodPostal'},
            'cod_postal': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judet': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'localitate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sector': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'strada': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tip_strada': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['adrese_postale']