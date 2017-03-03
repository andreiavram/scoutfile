# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photologue.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsociereEvenimentStructura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='Structur\u0103')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampArbitrarParticipareEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('tip_camp', models.CharField(max_length=255, choices=[(b'text', 'Text'), (b'number', 'Num\u0103r'), (b'bool', 'Bif\u0103'), (b'date', 'Dat\u0103')])),
                ('implicit', models.CharField(max_length=255, null=True, blank=True)),
                ('optional', models.BooleanField(default=True)),
                ('explicatii_suplimentare', models.CharField(help_text='Instruc\u021biuni despre cum s\u0103 fie completat acest c\xe2mp, format, ...', max_length=255, null=True, blank=True)),
                ('afiseaza_sumar', models.BooleanField(default=False, help_text='Afi\u0219eaz\u0103 totale la sf\xe2r\u0219itul tabelului', verbose_name='Afi\u0219eaz\u0103 sumar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetectedFace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Eveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=1024, verbose_name='Titlu')),
                ('descriere', models.TextField(null=True, blank=True)),
                ('start_date', models.DateTimeField(help_text='Folose\u0219te selectorul de date pentru a defini o dat\u0103 de \xeenceput', verbose_name='\xcencepe pe')),
                ('end_date', models.DateTimeField(help_text='Folose\u0219te selectorul de date pentru a defini o dat\u0103 de sf\xe2r\u0219it', verbose_name='\u021aine p\xe2n\u0103 pe')),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('tip_eveniment_text', models.CharField(default=b'alta', max_length=255, null=True, blank=True, choices=[(b'camp', b'Camp'), (b'intalnire', '\xcent\xe2lnire'), (b'hike', b'Hike'), (b'social', b'Proiect social'), (b'comunitate', 'Proiect de implicare \xeen comunitate'), (b'citychallange', 'City Challange'), (b'international', 'Proiect interna\u021bional'), (b'festival', 'Festival'), (b'ecologic', 'Proiect ecologic'), (b'alta', 'Alt tip de eveniment'), (b'training', 'Stagiu / training')])),
                ('facebook_event_link', models.URLField(help_text='Folose\u0219te copy/paste pentru a lua link-ul din Facebook', null=True, verbose_name='Link eveniment Facebook', blank=True)),
                ('articol_site_link', models.URLField(help_text='Link-ul de la articolul de pe site-ul Centrului Local', null=True, verbose_name='Link articol site', blank=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True, choices=[(b'propus', 'Propus'), (b'confirmat', 'Confirmat'), (b'derulare', '\xcen derulare'), (b'terminat', '\xcencheiat')])),
                ('locatie_text', models.CharField(max_length=1024, null=True, verbose_name='Loca\u021bie', blank=True)),
                ('locatie_geo', models.CharField(max_length=1024)),
                ('published_status', models.IntegerField(default=2, verbose_name='Vizibilitate', choices=[(1, b'Secret'), (2, b'Centru Local'), (3, b'Organiza\xc8\x9bie'), (4, b'Public')])),
                ('international', models.BooleanField(default=False, help_text='Dac\u0103 activitatea implic\u0103 participan\u021bi din alte \u021b\u0103ri sau are loc \xeen str\u0103in\u0103tate')),
                ('organizator', models.CharField(help_text='Dac\u0103 organizatorul este altul dec\xe2t Centrul Local, nota\u021bi-l aici', max_length=255, null=True, blank=True)),
                ('organizator_cercetas', models.BooleanField(default=True, help_text='Dac\u0103 organizatorul este un centru local sau ONCR, bifeaz\u0103 aici')),
                ('campuri_aditionale', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
                'ordering': ['-start_date'],
                'verbose_name': 'Eveniment',
                'verbose_name_plural': 'Evenimente',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EXIFData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'EXIFData',
                'verbose_name_plural': 'EXIFData',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlagReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('motiv', models.CharField(max_length=1024, choices=[(b'personal', 'Sunt \xeen poz\u0103 \u0219i nu sunt de acord s\u0103 apar\u0103 aici'), (b'ofensa', b'Consider c\xc4\x83 poza este ofensatoare'), (b'nonscout', b'Poza con\xc8\x9bine un comportament necercet\xc4\x83\xc8\x99esc \xc8\x99i nu ar trebui listat\xc4\x83 aici'), (b'calitateslaba', 'Poza este de calitate slab\u0103 \u0219i nu merit\u0103 p\u0103strat\u0103'), (b'altul', b'Alt motiv')])),
                ('alt_motiv', models.CharField(max_length=1024, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp', 'motiv'],
                'verbose_name': 'Raport poz\u0103',
                'verbose_name_plural': 'Rapoarte poze',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Imagine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=photologue.models.get_storage_path, max_length=1024, verbose_name='image')),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, editable=False, blank=True)),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count', editable=False)),
                ('crop_from', models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center'), (b'auto', 'Auto (Default)')])),
                ('data', models.DateTimeField(null=True, blank=True)),
                ('titlu', models.CharField(max_length=1024, null=True, blank=True)),
                ('descriere', models.TextField(null=True, blank=True)),
                ('resolution_x', models.IntegerField(null=True, blank=True)),
                ('resolution_y', models.IntegerField(null=True, blank=True)),
                ('score', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_flagged', models.BooleanField(default=False)),
                ('is_face_processed', models.BooleanField(default=False)),
                ('published_status', models.IntegerField(default=2, verbose_name='Vizibilitate', choices=[(1, b'Secret'), (2, b'Centru Local'), (3, b'Organiza\xc8\x9bie'), (4, b'Public')])),
            ],
            options={
                'ordering': ['date_taken'],
                'verbose_name': 'Imagine',
                'verbose_name_plural': 'Imagini',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstantaCampArbitrarParticipareEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valoare_text', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('prenume', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('telefon', models.CharField(max_length=255, null=True, blank=True)),
                ('adresa_postala', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantiEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alta_categorie', models.CharField(max_length=255, null=True, blank=True)),
                ('numar', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipareEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_sosire', models.DateTimeField(null=True, blank=True)),
                ('data_plecare', models.DateTimeField(null=True, blank=True)),
                ('status_participare', models.IntegerField(default=1, choices=[(1, 'Cu semnul \xeentreb\u0103rii'), (2, 'Confirmat'), (3, 'Avans pl\u0103tit'), (4, 'Participare efectiv\u0103'), (5, 'Participare anulat\u0103')])),
                ('detalii', models.TextField(null=True, blank=True)),
                ('rol', models.CharField(default=b'participant', max_length=255, choices=[(b'participant', 'Participant'), (b'insotitor', 'Lider \xeenso\u021bitor'), (b'invitat', 'Invitat'), (b'coordonator', 'Coordonator'), (b'staff', 'Membru staff')])),
                ('ultima_modificare', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-data_sosire'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RaportEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parteneri', models.TextField(help_text='C\xe2te unul pe linie, dac\u0103 exist\u0103 \u0219i un link va fi preluat automat de pe aceea\u0219i linie', null=True, blank=True)),
                ('obiective', models.TextField(help_text='inclusiv obiective educative', null=True, blank=True)),
                ('grup_tinta', models.TextField(null=True, blank=True)),
                ('activitati', models.TextField(help_text='Descriere semi-formal\u0103 a activit\u0103\u021bilor desf\u0103\u0219urate', null=True, blank=True)),
                ('alti_beneficiari', models.TextField(null=True, blank=True)),
                ('promovare', models.TextField(help_text='Cum / dac\u0103 s-a promovat proiectul', null=True, blank=True)),
                ('buget', models.FloatField(help_text='Estimativ, \xeen RON', null=True, blank=True)),
                ('accept_publicare_raport_national', models.BooleanField(default=True, help_text='Dac\u0103 se propune aceast\u0103 activitate pentru raportul anual al ONCR', verbose_name=b'Acord raport ONCR')),
                ('is_locked', models.BooleanField(default=False)),
                ('is_leaf', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SetPoze',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('autor', models.CharField(help_text='L\u0103sa\u021bi gol dac\u0103 \xeenc\u0103rca\u021bi pozele proprii', max_length=255, null=True, blank=True)),
                ('zip_file', models.FilePathField(path=b'/tmp', null=True, blank=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Initialized'), (1, b'Zip Uploaded'), (2, b'Zip queued for processing'), (3, b'Zip processed OK'), (4, b'Zip error')])),
                ('procent_procesat', models.IntegerField(default=0)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('offset_secunde', models.IntegerField(default=0, help_text=b'Num\xc4\x83rul de secunde cu care ceasul camerei voastre a fost decalat fa\xc8\x9b\xc4\x83 de ceasul corect (poate fi \xc8\x99i negativ). Foarte util pentru sincronizarea pozelor de la mai mul\xc8\x9bi fotografi')),
                ('offset_changed', models.BooleanField(default=False, verbose_name='Offset-ul a fost modificat')),
            ],
            options={
                'ordering': ['-date_uploaded'],
                'verbose_name': 'Set poze',
                'verbose_name_plural': 'seturi poze',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZiEveniment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('titlu', models.CharField(max_length=255)),
                ('descriere', models.TextField(null=True, blank=True)),
                ('index', models.IntegerField(default=1)),
                ('eveniment', models.ForeignKey(to='album.Eveniment')),
            ],
            options={
                'ordering': ['index', 'date'],
                'verbose_name': 'Zi eveniment',
                'verbose_name_plural': 'Zile eveniment',
            },
            bases=(models.Model,),
        ),
    ]
