# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import documente.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsociereDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('moment_asociere', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('data_inregistrare', models.DateField(null=True, blank=True)),
                ('titlu', models.CharField(max_length=1024)),
                ('descriere', models.CharField(max_length=2048, null=True, blank=True)),
                ('fisier', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/media/', location=b'/vagrant/media'), null=True, upload_to=documente.models.upload_to_document_fisier, blank=True)),
                ('url', models.URLField(max_length=2048, null=True, blank=True)),
                ('version_number', models.IntegerField(default=0)),
                ('locked', models.BooleanField(default=False)),
                ('is_folder', models.BooleanField(default=False)),
                ('fragment', models.IntegerField(default=0)),
                ('numar_inregistrare', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Decizie',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Document')),
                ('continut', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('documente.document',),
        ),
        migrations.CreateModel(
            name='DecizieRezervareNumere',
            fields=[
                ('decizie_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Decizie')),
                ('tip_rezervare', models.CharField(max_length=255, choices=[(b'chitantier', 'Chitan\u021bier'), (b'facturier', 'Facturier'), (b'io', 'Registru intr\u0103ri / ie\u0219iri'), (b'intern', 'Registru intern')])),
                ('automat', models.BooleanField(default=True)),
                ('numar_inceput', models.IntegerField()),
                ('numar_sfarsit', models.IntegerField(null=True, blank=True)),
                ('serie', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=('documente.decizie',),
        ),
        migrations.CreateModel(
            name='DecizieCotizatie',
            fields=[
                ('decizie_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Decizie')),
                ('cuantum', models.FloatField(help_text='Valoare exprimat\u0103 \xeen RON pentru un an calendaristic (4 trimestre)')),
                ('categorie', models.CharField(default=b'normal', max_length=255, choices=[(b'local', 'Local'), (b'national', 'Na\u021bional'), (b'local-social', 'Local (social)'), (b'national-social', 'Na\u021bional (social)')])),
                ('data_inceput', models.DateField()),
                ('data_sfarsit', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=('documente.decizie',),
        ),
        migrations.CreateModel(
            name='Chitanta',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Document')),
                ('suma', models.FloatField(default=0)),
                ('printata', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('documente.document',),
        ),
        migrations.CreateModel(
            name='ChitantaCotizatie',
            fields=[
                ('chitanta_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Chitanta')),
                ('predat', models.BooleanField(default=False)),
                ('blocat', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('documente.chitanta',),
        ),
        migrations.CreateModel(
            name='DocumentCotizatieSociala',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='documente.Document')),
                ('nume_parinte', models.CharField(help_text='Las\u0103 gol pentru cerceta\u0219i adul\u021bi', max_length=255, null=True, verbose_name='Nume p\u0103rinte', blank=True)),
                ('motiv', models.CharField(max_length=2048, null=True, blank=True)),
                ('este_valabil', models.BooleanField(default=False, help_text='Bifeaz\u0103 doar dac\u0103 cererea a fost aprobat\u0103 de Consiliu', verbose_name='Cerere aprobat\u0103?')),
                ('valabilitate_start', models.DateField()),
                ('valabilitate_end', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=('documente.document',),
        ),
        migrations.CreateModel(
            name='PlataCotizatieTrimestru',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('partial', models.BooleanField(default=False)),
                ('final', models.BooleanField(default=False)),
                ('suma', models.FloatField()),
                ('index', models.IntegerField()),
                ('tip_inregistrare', models.CharField(default=b'normal', max_length=255, choices=[(b'normal', 'Plat\u0103 normal\u0103'), (b'inactiv', b'Inactiv')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registru',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mod_functionare', models.CharField(default=b'auto', help_text='Registrul cu numerotare automat\u0103 \xee\u0219i gestioneaz\u0103 singur numerele de \xeenregistrare', max_length=255, verbose_name='Tip numerotare', choices=[(b'auto', 'Automat'), (b'manual', 'Manual')])),
                ('tip_registru', models.CharField(max_length=255, choices=[(b'chitantier', 'Chitan\u021bier'), (b'facturier', 'Facturier'), (b'io', 'Registru intr\u0103ri / ie\u0219iri'), (b'intern', 'Registru intern')])),
                ('serie', models.CharField(max_length=255, null=True, blank=True)),
                ('numar_inceput', models.IntegerField(default=1)),
                ('numar_sfarsit', models.IntegerField(null=True, blank=True)),
                ('numar_curent', models.IntegerField()),
                ('valabil', models.BooleanField(default=True)),
                ('editabil', models.BooleanField(default=True)),
                ('data_inceput', models.DateTimeField(auto_now_add=True)),
                ('descriere', models.TextField(help_text='Un scurt text de descriere pentru registru', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipAsociereDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('slug', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=255)),
                ('nume', models.CharField(max_length=255)),
                ('descriere', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trimestru',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_inceput', models.DateField()),
                ('data_sfarsit', models.DateField()),
                ('ordine_locala', models.PositiveSmallIntegerField()),
                ('ordine_globala', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
