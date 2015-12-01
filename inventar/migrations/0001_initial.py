# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0005_auto_20151130_0205'),
        ('documente', '0004_auto_20150330_0018'),
        ('album', '0007_auto_20151130_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieInventar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('responsabil', models.ForeignKey(to='structuri.Membru')),
            ],
        ),
        migrations.CreateModel(
            name='IesireInventar',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Document')),
                ('cantitate_scoasa', models.PositiveIntegerField(null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('motiv', models.CharField(max_length=255, choices=[(b'activitate', 'Activitate'), (b'imprumut', '\xcemprumut'), (b'casare', 'Casare'), (b'distrugere', 'Distrugere')])),
                ('activitate', models.ForeignKey(to='album.Eveniment')),
            ],
            bases=('documente.document',),
        ),
        migrations.CreateModel(
            name='IntrareInventar',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Document')),
                ('cantitate_intrata', models.PositiveIntegerField(null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('observatii', models.TextField(null=True, blank=True)),
                ('iesire_inventar', models.ForeignKey(blank=True, to='inventar.IesireInventar', null=True)),
            ],
            bases=('documente.document',),
        ),
        migrations.CreateModel(
            name='LocateiInventar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('centru_local', models.ForeignKey(to='structuri.CentruLocal')),
                ('responsabil', models.ForeignKey(to='structuri.Membru')),
            ],
        ),
        migrations.CreateModel(
            name='ObiectInventar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('denumire', models.CharField(max_length=255)),
                ('descriere', models.TextField(null=True, blank=True)),
                ('cod_inventar', models.CharField(max_length=255)),
                ('multi_part', models.BooleanField(default=False)),
                ('unitate_de_masura', models.CharField(max_length=255)),
                ('cantitate_curenta', models.PositiveIntegerField(default=1)),
                ('stare', models.CharField(max_length=255, choices=[(b'nou', 'Nou'), (b'fb', 'Foarte bun\u0103'), (b'b', 'Bun\u0103'), (b'u', 'Utilizabil'), (b'r', 'Are nevoie de repara\u021bii'), (b'p', 'Proast\u0103')])),
                ('categorie', models.ForeignKey(blank=True, to='inventar.CategorieInventar', null=True)),
                ('locatie', models.ForeignKey(to='inventar.LocateiInventar')),
                ('responsabil', models.ForeignKey(to='structuri.Membru')),
            ],
        ),
        migrations.AddField(
            model_name='intrareinventar',
            name='ref_obiect_inventar',
            field=models.ForeignKey(to='inventar.ObiectInventar'),
        ),
        migrations.AddField(
            model_name='intrareinventar',
            name='responsabil',
            field=models.ForeignKey(to='structuri.Membru'),
        ),
        migrations.AddField(
            model_name='iesireinventar',
            name='ref_obiect_inventar',
            field=models.ForeignKey(to='inventar.ObiectInventar'),
        ),
        migrations.AddField(
            model_name='iesireinventar',
            name='responsabil',
            field=models.ForeignKey(to='structuri.Membru'),
        ),
    ]
