# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cantece
import django.core.files.storage
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cantec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume_fisier', models.FilePathField(verbose_name=b'/vagrant/media/cartecantece/cantece')),
                ('titlu', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=1024)),
                ('cover_photo', models.ImageField(null=True, upload_to=cantece.models.upload_to_cover_photo, blank=True)),
                ('album', models.CharField(max_length=255, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarteCantece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConexiuneCantecCarte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=255, choices=[(b'propus', 'Propus'), (b'aprobat', 'Aprobat'), (b'respins', 'Respins')])),
                ('cantec', models.ForeignKey(to='cantece.Cantec')),
                ('carte', models.ForeignKey(to='cantece.CarteCantece')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptiuniTemplateCarteCantece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('descriere', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateCarteCantece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('template_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/media/', location=b'/vagrant/media'), upload_to=cantece.models.upload_to_template_carte_cantece)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='optiunitemplatecartecantece',
            name='template',
            field=models.ForeignKey(to='cantece.TemplateCarteCantece'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartecantece',
            name='cantece',
            field=models.ManyToManyField(to='cantece.Cantec', through='cantece.ConexiuneCantecCarte'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartecantece',
            name='optiuni_template',
            field=models.ManyToManyField(to='cantece.OptiuniTemplateCarteCantece', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartecantece',
            name='template',
            field=models.ForeignKey(to='cantece.TemplateCarteCantece'),
            preserve_default=True,
        ),
    ]
