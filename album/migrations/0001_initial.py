# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Eveniment'
        db.create_table('album_eveniment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centru_local', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structuri.CentruLocal'])),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descriere', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('album', ['Eveniment'])

        # Adding model 'ZiEveniment'
        db.create_table('album_zieveniment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eveniment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Eveniment'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('titlu', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descriere', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('album', ['ZiEveniment'])

        # Adding model 'SetPoze'
        db.create_table('album_setpoze', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eveniment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Eveniment'])),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('album', ['SetPoze'])

        # Adding model 'Imagine'
        db.create_table('album_imagine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1024)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(default='center', max_length=10, blank=True)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imagine_related', null=True, to=orm['photologue.PhotoEffect'])),
            ('set_poze', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.SetPoze'])),
            ('data', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('titlu', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('descriere', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('resolution_x', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('resolution_y', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('album', ['Imagine'])

        # Adding model 'EXIFData'
        db.create_table('album_exifdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imagine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Imagine'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('album', ['EXIFData'])


    def backwards(self, orm):
        
        # Deleting model 'Eveniment'
        db.delete_table('album_eveniment')

        # Deleting model 'ZiEveniment'
        db.delete_table('album_zieveniment')

        # Deleting model 'SetPoze'
        db.delete_table('album_setpoze')

        # Deleting model 'Imagine'
        db.delete_table('album_imagine')

        # Deleting model 'EXIFData'
        db.delete_table('album_exifdata')


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
        'album.imagine': {
            'Meta': {'ordering': "['date_taken']", 'object_name': 'Imagine'},
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imagine_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024'}),
            'resolution_x': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'resolution_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'set_poze': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.SetPoze']"}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'album.setpoze': {
            'Meta': {'object_name': 'SetPoze'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'album.zieveniment': {
            'Meta': {'ordering': "['date']", 'object_name': 'ZiEveniment'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
