# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cantec'
        db.create_table('cantece_cantec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume_fisier', self.gf('django.db.models.fields.FilePathField')(max_length=100)),
            ('titlu', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('cover_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('album', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('cantece', ['Cantec'])

        # Adding model 'OptiuniTemplateCarteCantece'
        db.create_table('cantece_optiunitemplatecartecantece', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descriere', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cantece.TemplateCarteCantece'])),
        ))
        db.send_create_signal('cantece', ['OptiuniTemplateCarteCantece'])

        # Adding model 'TemplateCarteCantece'
        db.create_table('cantece_templatecartecantece', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nume', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('template_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('cantece', ['TemplateCarteCantece'])

        # Adding model 'CarteCantece'
        db.create_table('cantece_cartecantece', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cantece.TemplateCarteCantece'])),
        ))
        db.send_create_signal('cantece', ['CarteCantece'])

        # Adding M2M table for field optiuni_template on 'CarteCantece'
        m2m_table_name = db.shorten_name('cantece_cartecantece_optiuni_template')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cartecantece', models.ForeignKey(orm['cantece.cartecantece'], null=False)),
            ('optiunitemplatecartecantece', models.ForeignKey(orm['cantece.optiunitemplatecartecantece'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cartecantece_id', 'optiunitemplatecartecantece_id'])

        # Adding model 'ConexiuneCantecCarte'
        db.create_table('cantece_conexiunecanteccarte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cantec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cantece.Cantec'])),
            ('carte', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cantece.CarteCantece'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('cantece', ['ConexiuneCantecCarte'])


    def backwards(self, orm):
        # Deleting model 'Cantec'
        db.delete_table('cantece_cantec')

        # Deleting model 'OptiuniTemplateCarteCantece'
        db.delete_table('cantece_optiunitemplatecartecantece')

        # Deleting model 'TemplateCarteCantece'
        db.delete_table('cantece_templatecartecantece')

        # Deleting model 'CarteCantece'
        db.delete_table('cantece_cartecantece')

        # Removing M2M table for field optiuni_template on 'CarteCantece'
        db.delete_table(db.shorten_name('cantece_cartecantece_optiuni_template'))

        # Deleting model 'ConexiuneCantecCarte'
        db.delete_table('cantece_conexiunecanteccarte')


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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'cantece.cantec': {
            'Meta': {'object_name': 'Cantec'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'cover_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume_fisier': ('django.db.models.fields.FilePathField', [], {'max_length': '100'}),
            'titlu': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cantece.cartecantece': {
            'Meta': {'object_name': 'CarteCantece'},
            'cantece': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cantece.Cantec']", 'through': "orm['cantece.ConexiuneCantecCarte']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optiuni_template': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cantece.OptiuniTemplateCarteCantece']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cantece.TemplateCarteCantece']"})
        },
        'cantece.conexiunecanteccarte': {
            'Meta': {'object_name': 'ConexiuneCantecCarte'},
            'cantec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cantece.Cantec']"}),
            'carte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cantece.CarteCantece']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cantece.optiunitemplatecartecantece': {
            'Meta': {'object_name': 'OptiuniTemplateCarteCantece'},
            'descriere': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cantece.TemplateCarteCantece']"})
        },
        'cantece.templatecartecantece': {
            'Meta': {'object_name': 'TemplateCarteCantece'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nume': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['cantece']