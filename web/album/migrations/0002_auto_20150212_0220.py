# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('photologue', '__first__'),
        ('album', '0001_initial'),
        ('structuri', '0001_initial'),
        ('proiecte', '0002_auto_20150212_0220'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setpoze',
            name='autor_user',
            field=models.ForeignKey(blank=True, to='structuri.Membru', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='setpoze',
            name='eveniment',
            field=models.ForeignKey(to='album.Eveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='editor',
            field=models.ForeignKey(to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='eveniment',
            field=models.ForeignKey(to='album.Eveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='original_parent',
            field=models.ForeignKey(blank=True, to='album.RaportEveniment', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='album.RaportEveniment', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participareeveniment',
            name='eveniment',
            field=models.ForeignKey(to='album.Eveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participareeveniment',
            name='membru',
            field=models.ForeignKey(blank=True, to='structuri.Membru', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participareeveniment',
            name='nonmembru',
            field=models.ForeignKey(blank=True, to='album.ParticipantEveniment', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participareeveniment',
            name='user_modificare',
            field=models.ForeignKey(related_name='participari_responsabil', blank=True, to='structuri.Membru', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participantieveniment',
            name='eveniment',
            field=models.ForeignKey(to='album.Eveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participantieveniment',
            name='ramura_de_varsta',
            field=models.ForeignKey(blank=True, to='structuri.RamuraDeVarsta', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instantacamparbitrarparticipareeveniment',
            name='camp',
            field=models.ForeignKey(related_name='instante', to='album.CampArbitrarParticipareEveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instantacamparbitrarparticipareeveniment',
            name='participare',
            field=models.ForeignKey(to='album.ParticipareEveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagine',
            name='effect',
            field=models.ForeignKey(related_name='imagine_related', verbose_name='effect', blank=True, to='photologue.PhotoEffect', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagine',
            name='set_poze',
            field=models.ForeignKey(blank=True, to='album.SetPoze', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagine',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flagreport',
            name='imagine',
            field=models.ForeignKey(to='album.Imagine', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exifdata',
            name='imagine',
            field=models.ForeignKey(to='album.Imagine', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eveniment',
            name='centru_local',
            field=models.ForeignKey(to='structuri.CentruLocal', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eveniment',
            name='custom_cover_photo',
            field=models.ForeignKey(blank=True, to='album.Imagine', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eveniment',
            name='proiect',
            field=models.ForeignKey(blank=True, to='proiecte.Project', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eveniment',
            name='responsabil_articol',
            field=models.ForeignKey(related_name='evenimente_articol', blank=True, to='structuri.Membru', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eveniment',
            name='responsabil_raport',
            field=models.ForeignKey(related_name='evenimente_raport', blank=True, to='structuri.Membru', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eveniment',
            name='tip_eveniment',
            field=models.ForeignKey(to='album.TipEveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detectedface',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detectedface',
            name='imagine',
            field=models.ForeignKey(to='album.Imagine', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camparbitrarparticipareeveniment',
            name='eveniment',
            field=models.ForeignKey(to='album.Eveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asociereevenimentstructura',
            name='content_type',
            field=models.ForeignKey(verbose_name='Tip structur\u0103', to='contenttypes.ContentType', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asociereevenimentstructura',
            name='eveniment',
            field=models.ForeignKey(to='album.Eveniment', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
