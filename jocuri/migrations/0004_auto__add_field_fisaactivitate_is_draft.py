# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FisaActivitate.is_draft'
        db.add_column('jocuri_fisaactivitate', 'is_draft',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FisaActivitate.is_draft'
        db.delete_column('jocuri_fisaactivitate', 'is_draft')


    models = {
        'album.eveniment': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Eveniment'},
            'articol_site_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'centru_local': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.CentruLocal']"}),
            'custom_cover_photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']", 'null': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'facebook_event_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locatie_geo': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'locatie_text': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'organizator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organizator_cercetas': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'proiect': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proiecte.Project']", 'null': 'True', 'blank': 'True'}),
            'published_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'responsabil_articol': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evenimente_articol'", 'null': 'True', 'to': "orm['structuri.Membru']"}),
            'responsabil_raport': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evenimente_raport'", 'null': 'True', 'to': "orm['structuri.Membru']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tip_eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.TipEveniment']"}),
            'tip_eveniment_text': ('django.db.models.fields.CharField', [], {'default': "'alta'", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'album.imagine': {
            'Meta': {'ordering': "['date_taken']", 'object_name': 'Imagine'},
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'set_poze': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.SetPoze']", 'null': 'True', 'blank': 'True'}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'album.setpoze': {
            'Meta': {'ordering': "['-date_uploaded']", 'object_name': 'SetPoze'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'autor_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']", 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'eveniment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset_changed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offset_secunde': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'procent_procesat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'zip_file': ('django.db.models.fields.FilePathField', [], {'max_length': '100', 'path': "'/tmp'", 'null': 'True', 'blank': 'True'})
        },
        'album.tipeveniment': {
            'Meta': {'object_name': 'TipEveniment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'documente.document': {
            'Meta': {'object_name': 'Document'},
            'data_inregistrare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'fisier': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fisiere'", 'null': 'True', 'to': "orm['documente.Document']"}),
            'fragment': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_storage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']", 'null': 'True', 'blank': 'True'}),
            'is_folder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numar_inregistrare': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'registru': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documente.Registru']", 'null': 'True', 'blank': 'True'}),
            'root_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'versions'", 'null': 'True', 'to': "orm['documente.Document']"}),
            'tip_document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documente.TipDocument']", 'null': 'True', 'blank': 'True'}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'version_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'documente.registru': {
            'Meta': {'object_name': 'Registru'},
            'centru_local': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.CentruLocal']"}),
            'data_inceput': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_referinta': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registru_referinta'", 'null': 'True', 'to': "orm['documente.Document']"}),
            'editabil': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_functionare': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '255'}),
            'numar_curent': ('django.db.models.fields.IntegerField', [], {}),
            'numar_inceput': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'numar_sfarsit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']"}),
            'serie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tip_registru': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'valabil': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'documente.tipdocument': {
            'Meta': {'object_name': 'TipDocument'},
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'documente.trimestru': {
            'Meta': {'object_name': 'Trimestru'},
            'data_inceput': ('django.db.models.fields.DateField', [], {}),
            'data_sfarsit': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordine_globala': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordine_locala': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'jocuri.categoriefiseactivitate': {
            'Meta': {'object_name': 'CategorieFiseActivitate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'jocuri.fisaactivitate': {
            'Meta': {'object_name': 'FisaActivitate', '_ormbases': ['documente.Document']},
            'categorie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jocuri.CategorieFiseActivitate']"}),
            'descriere_joc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['documente.Document']", 'unique': 'True', 'primary_key': 'True'}),
            'editori': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structuri.Membru']", 'symmetrical': 'False'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'materiale_necesare': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'max_durata': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_participanti': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_durata': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_participanti': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obiective_educative': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ramuri_de_varsta': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['structuri.RamuraDeVarsta']", 'null': 'True', 'blank': 'True'}),
            'sursa': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
        'proiecte.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'visibility': ('django.db.models.fields.IntegerField', [], {})
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
            'activa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'antet': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'denumire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localitate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        'structuri.ramuradevarsta': {
            'Meta': {'object_name': 'RamuraDeVarsta'},
            'are_patrule': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'culoare': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'varsta_iesire': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'varsta_intrare': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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

    complete_apps = ['jocuri']