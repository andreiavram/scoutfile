# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Eveniment.locatie_long'
        db.delete_column('album_eveniment', 'locatie_long')

        # Deleting field 'Eveniment.locatie_lat'
        db.delete_column('album_eveniment', 'locatie_lat')

        # Adding field 'Eveniment.locatie_geo'
        db.add_column('album_eveniment', 'locatie_geo',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1024),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Eveniment.locatie_long'
        db.add_column('album_eveniment', 'locatie_long',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Eveniment.locatie_lat'
        db.add_column('album_eveniment', 'locatie_lat',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'Eveniment.locatie_geo'
        db.delete_column('album_eveniment', 'locatie_geo')


    models = {
        'album.detectedface': {
            'Meta': {'object_name': 'DetectedFace'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        'album.eveniment': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Eveniment'},
            'centru_local': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.CentruLocal']"}),
            'custom_cover_photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']", 'null': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'facebook_event_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locatie_geo': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'locatie_text': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
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
            'is_face_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'resolution_x': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'resolution_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'set_poze': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.SetPoze']"}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'album.participareeveniment': {
            'Meta': {'object_name': 'ParticipareEveniment'},
            'data_plecare': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'data_sosire': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'detalii': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']"}),
            'status_participare': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'album.setpoze': {
            'Meta': {'ordering': "['-date_uploaded']", 'object_name': 'SetPoze'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autor_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']", 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset_secunde': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'procent_procesat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'zip_file': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'path': "'/tmp'", 'null': 'True', 'blank': 'True'})
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
        'documente.trimestru': {
            'Meta': {'object_name': 'Trimestru'},
            'data_inceput': ('django.db.models.fields.DateField', [], {}),
            'data_sfarsit': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordine_globala': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordine_locala': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
        'structuri.asocieremembrufamilie': {
            'Meta': {'object_name': 'AsociereMembruFamilie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persoana_destinatie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membru_destinatie'", 'to': "orm['structuri.Membru']"}),
            'persoana_sursa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']"}),
            'tip_relatie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TipRelatieFamilie']"})
        },
        'structuri.centrulocal': {
            'Meta': {'object_name': 'CentruLocal'},
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'denumire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localitate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'moment_initial_cotizatie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documente.Trimestru']", 'null': 'True', 'blank': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'preferinte_corespondenta': ('django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '255'}),
            'specific': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'statut_drepturi': ('django.db.models.fields.CharField', [], {'default': "'depline'", 'max_length': '255'}),
            'statut_juridic': ('django.db.models.fields.CharField', [], {'default': "'nopj'", 'max_length': '255'})
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
            'cnp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'data_nasterii': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'familie': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['structuri.Membru']", 'null': 'True', 'through': "orm['structuri.AsociereMembruFamilie']", 'blank': 'True'}),
            'poza_profil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.ImagineProfil']", 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'telefon': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'utilizator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['structuri.Utilizator']", 'unique': 'True', 'primary_key': 'True'})
        },
        'structuri.tiprelatiefamilie': {
            'Meta': {'object_name': 'TipRelatieFamilie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reverse_relationship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TipRelatieFamilie']", 'null': 'True', 'blank': 'True'})
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
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['album']