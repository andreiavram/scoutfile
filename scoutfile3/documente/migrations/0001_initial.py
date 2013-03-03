# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Document'
        db.create_table('documente_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('titlu', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('descriere', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('fisier', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2048, null=True, blank=True)),
            ('version_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('root_document', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='versions', null=True, to=orm['documente.Document'])),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='folder_parinte', null=True, to=orm['documente.Document'])),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_folder', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('documente', ['Document'])

        # Adding model 'TipAsociereDocument'
        db.create_table('documente_tipasocieredocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('documente', ['TipAsociereDocument'])

        # Adding model 'AsociereDocument'
        db.create_table('documente_asocieredocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documente.Document'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tip_asociere', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documente.TipAsociereDocument'], null=True, blank=True)),
            ('moment_asociere', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('responsabil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('documente', ['AsociereDocument'])


    def backwards(self, orm):
        
        # Deleting model 'Document'
        db.delete_table('documente_document')

        # Deleting model 'TipAsociereDocument'
        db.delete_table('documente_tipasocieredocument')

        # Deleting model 'AsociereDocument'
        db.delete_table('documente_asocieredocument')


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
        'documente.asocieredocument': {
            'Meta': {'object_name': 'AsociereDocument'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documente.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment_asociere': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'responsabil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'tip_asociere': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documente.TipAsociereDocument']", 'null': 'True', 'blank': 'True'})
        },
        'documente.document': {
            'Meta': {'object_name': 'Document'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'fisier': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'folder_parinte'", 'null': 'True', 'to': "orm['documente.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_folder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'root_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'versions'", 'null': 'True', 'to': "orm['documente.Document']"}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'version_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'documente.tipasocieredocument': {
            'Meta': {'object_name': 'TipAsociereDocument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['documente']
