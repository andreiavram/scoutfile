# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('documente', '0001_initial'),
        ('album', '0002_auto_20150212_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='registru',
            name='centru_local',
            field=models.ForeignKey(to='structuri.CentruLocal', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registru',
            name='document_referinta',
            field=models.ForeignKey(related_name='registru_referinta', blank=True, to='documente.Document', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registru',
            name='owner',
            field=models.ForeignKey(to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='platacotizatietrimestru',
            name='chitanta',
            field=models.ForeignKey(blank=True, to='documente.ChitantaCotizatie', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='platacotizatietrimestru',
            name='membru',
            field=models.ForeignKey(to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='platacotizatietrimestru',
            name='trimestru',
            field=models.ForeignKey(to='documente.Trimestru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=models.ForeignKey(related_name='fisiere', blank=True, to='documente.Document', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='image_storage',
            field=models.ForeignKey(blank=True, to='album.Imagine', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='registru',
            field=models.ForeignKey(blank=True, to='documente.Registru', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='root_document',
            field=models.ForeignKey(related_name='versions', blank=True, to='documente.Document', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='tip_document',
            field=models.ForeignKey(blank=True, to='documente.TipDocument', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decizie',
            name='centru_local',
            field=models.ForeignKey(to='structuri.CentruLocal', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chitanta',
            name='casier',
            field=models.ForeignKey(to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieredocument',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieredocument',
            name='document',
            field=models.ForeignKey(to='documente.Document', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieredocument',
            name='document_ctype',
            field=models.ForeignKey(related_name='asociere', blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieredocument',
            name='responsabil',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieredocument',
            name='tip_asociere',
            field=models.ForeignKey(blank=True, to='documente.TipAsociereDocument', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Adeziune',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('documente.document',),
        ),
    ]
