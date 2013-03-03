# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SetPoze.offset_secunde'
        db.add_column('album_setpoze', 'offset_secunde', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SetPoze.offset_secunde'
        db.delete_column('album_setpoze', 'offset_secunde')


    models = {
        'album.eveniment': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Eveniment'},
            'centru_local': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.CentruLocal']"}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'album.exifdata': {
            'Meta': {'object_name': 'EXIFData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'album.flagreport': {
            'Meta': {'ordering': "['-timestamp', 'motiv']", 'object_name': 'FlagReport'},
            'alt_motiv': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']"}),
            'motiv': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'album.imagine': {
            'Meta': {'ordering': "['date_taken']", 'object_name': 'Imagine'},
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imagine_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resolution_x': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'resolution_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'set_poze': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.SetPoze']"}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'album.setpoze': {
            'Meta': {'object_name': 'SetPoze'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset_secunde': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'album.zieveniment': {
            'Meta': {'ordering': "['date']", 'object_name': 'ZiEveniment'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'structuri.centrulocal': {
            'Meta': {'object_name': 'CentruLocal'},
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'denumire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localitate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'specific': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['album']
