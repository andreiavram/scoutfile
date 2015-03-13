# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('structuri', '0001_initial'),
        ('documente', '0002_auto_20150212_0220'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieFiseActivitate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FisaActivitate',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Document')),
                ('descriere_joc', models.TextField(null=True, verbose_name='Descriere', blank=True)),
                ('materiale_necesare', models.TextField(help_text='C\xe2te unul pe linie, f\u0103r\u0103 numerotare adi\u021bional\u0103', null=True, blank=True)),
                ('min_participanti', models.PositiveIntegerField(null=True, verbose_name='Minim participan\u021bi', blank=True)),
                ('max_participanti', models.PositiveIntegerField(null=True, verbose_name='Maxim participan\u021bi', blank=True)),
                ('min_durata', models.PositiveIntegerField(help_text='Folose\u0219te expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m', null=True, verbose_name='Durata minim\u0103', blank=True)),
                ('max_durata', models.PositiveIntegerField(help_text='Folose\u0219te expresii de tipul 2h15m sau 1z3h30m sau 2h sau 12m', null=True, verbose_name='Durata maxim\u0103', blank=True)),
                ('obiective_educative', models.TextField(help_text='C\xe2te unul pe linie, f\u0103r\u0103 numerotare (se va face automat)', null=True, blank=True)),
                ('sursa', models.CharField(help_text='De unde a\u021bi adus jocul / activitatea asta \xeen grupul vostru', max_length=255, null=True, blank=True)),
                ('is_draft', models.BooleanField(default=True, help_text='Dac\u0103 nu e\u0219ti chiar gata, marcheaz\u0103 bifa aici ca s\u0103 \u0219tie \u0219i ceilal\u021bi', verbose_name='Este incomplet?')),
                ('categorie', models.ForeignKey(to='jocuri.CategorieFiseActivitate')),
                ('editori', models.ManyToManyField(to='structuri.Membru')),
                ('ramuri_de_varsta', models.ManyToManyField(to='structuri.RamuraDeVarsta', null=True, blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=('documente.document',),
        ),
    ]
