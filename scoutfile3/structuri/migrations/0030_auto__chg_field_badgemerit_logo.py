# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BadgeMerit.logo'
        db.alter_column('structuri_badgemerit', 'logo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Imagine'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'BadgeMerit.logo'
        raise RuntimeError("Cannot reverse this migration. 'BadgeMerit.logo' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'BadgeMerit.logo'
        db.alter_column('structuri_badgemerit', 'logo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Imagine']))

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
        'structuri.badgemerit': {
            'Meta': {'object_name': 'BadgeMerit'},
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'etapa_progres': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.EtapaProgres']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']", 'null': 'True', 'blank': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ramura_de_varsta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.RamuraDeVarsta']", 'null': 'True', 'blank': 'True'})
        },
        'structuri.badgemeritmembru': {
            'Meta': {'object_name': 'BadgeMeritMembru'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.BadgeMerit']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'detalii': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'evaluator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'badgeuri_merit_evaluate'", 'to': "orm['structuri.Membru']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'badgeuri_merit'", 'to': "orm['structuri.Membru']"})
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
        'structuri.etapaprogres': {
            'Meta': {'object_name': 'EtapaProgres'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Imagine']"}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordine': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ramura_de_varsta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.RamuraDeVarsta']"}),
            'reguli': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'structuri.etapaprogresmembru': {
            'Meta': {'object_name': 'EtapaProgresMembru'},
            'data': ('django.db.models.fields.DateField', [], {}),
            'detalii': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'etapa_progres': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.EtapaProgres']"}),
            'evaluator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'etape_progres_evaluate'", 'to': "orm['structuri.Membru']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'etape_progres'", 'to': "orm['structuri.Membru']"})
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
        'structuri.informatiecontact': {
            'Meta': {'object_name': 'InformatieContact'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'data_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'data_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'informatii_suplimentare': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'obiect_ref_ctype': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'referit'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'obiect_ref_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tip_informatie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TipInformatieContact']"}),
            'valoare': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
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
        'structuri.notatargetetapaprogres': {
            'Meta': {'object_name': 'NotaTargetEtapaProgres'},
            'activitate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']", 'null': 'True', 'blank': 'True'}),
            'evaluator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'note_etape_progres_evaluate'", 'to': "orm['structuri.Membru']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'note_etape_progres'", 'to': "orm['structuri.Membru']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TargetEtapaProgres']"}),
            'target_atins': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'structuri.noteobiectivprogresmembru': {
            'Meta': {'object_name': 'NoteObiectivProgresMembru'},
            'activitate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Eveniment']", 'null': 'True', 'blank': 'True'}),
            'etapa_progres': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.EtapaProgres']"}),
            'evaluator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'note_obiective_progres_evaluate'", 'to': "orm['structuri.Membru']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'note_obiective_progres'", 'to': "orm['structuri.Membru']"}),
            'nota': ('django.db.models.fields.TextField', [], {}),
            'obiectiv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.ObiectivEducativProgres']"}),
            'obiectiv_atins': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'structuri.obiectiveducativprogres': {
            'Meta': {'object_name': 'ObiectivEducativProgres'},
            'descriere': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domeniu': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pista': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'structuri.patrula': {
            'Meta': {'object_name': 'Patrula'},
            'activa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data_infiintare': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment_inchidere': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unitate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Unitate']"})
        },
        'structuri.persoanadecontact': {
            'Meta': {'object_name': 'PersoanaDeContact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implicit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'membru': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.Membru']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telefon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tip_relatie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TipRelatieFamilie']", 'null': 'True', 'blank': 'True'})
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
        'structuri.targetetapaprogres': {
            'Meta': {'object_name': 'TargetEtapaProgres'},
            'capitol': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'structuri.tipasocieremembrustructura': {
            'Meta': {'object_name': 'TipAsociereMembruStructura'},
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'structuri.tipinformatiecontact': {
            'Meta': {'object_name': 'TipInformatieContact'},
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sms_capable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'relevanta': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'structuri.tiprelatiefamilie': {
            'Meta': {'object_name': 'TipRelatieFamilie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reverse_relationship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structuri.TipRelatieFamilie']", 'null': 'True', 'blank': 'True'})
        },
        'structuri.unitate': {
            'Meta': {'object_name': 'Unitate'},
            'activa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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

    complete_apps = ['structuri']