# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TipAsociereMembruStructura.content_type'
        db.add_column('structuri_tipasocieremembrustructura', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'TipAsociereMembruStructura.content_type'
        db.delete_column('structuri_tipasocieremembrustructura', 'content_type_id')


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
        'structuri.asocieremembrustructura': {
            'Meta': {'object_name': 'AsociereMembruStructura'},
            'confirmata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmata_de': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'asocieri_confirmate'", 'null': 'True', 'to': "orm['structuri.Utilizator']"}),
            'confirmata_pe': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'afilieri'", 'to': "orm['structuri.Membru']"}),
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
        'structuri.imagineprofil': {
            'Meta': {'object_name': 'ImagineProfil'},
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imagineprofil_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'structuri.membru': {
            'Meta': {'object_name': 'Membru', '_ormbases': ['structuri.Utilizator']},
            'adresa': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'centru_local': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.CentruLocal']", 'null': 'True', 'blank': 'True'}),
            'cnp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'data_nasterii': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'poza_profil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.ImagineProfil']", 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
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
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'requested_password_reset': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp_confirmed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp_registered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['structuri']
