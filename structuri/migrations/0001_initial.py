# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photologue.models
import structuri.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documente', '0001_initial'),
        ('photologue', '__first__'),
        ('contenttypes', '0001_initial'),
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsociereMembruFamilie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AsociereMembruStructura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='Structur\u0103')),
                ('moment_inceput', models.DateTimeField(null=True, blank=True)),
                ('moment_incheiere', models.DateTimeField(null=True, blank=True)),
                ('confirmata', models.BooleanField(default=False)),
                ('confirmata_pe', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BadgeMerit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('descriere', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BadgeMeritMembru',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField()),
                ('detalii', models.TextField(null=True, blank=True)),
                ('badge', models.ForeignKey(to='structuri.BadgeMerit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CentruLocal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('data_infiintare', models.DateField(null=True, blank=True)),
                ('activa', models.BooleanField(default=True)),
                ('localitate', models.CharField(max_length=255)),
                ('denumire', models.CharField(max_length=255, null=True, blank=True)),
                ('specific', models.CharField(blank=True, max_length=255, null=True, choices=[(b'catolic', b'Catolic'), (b'marinaresc', 'Marin\u0103resc')])),
                ('statut_juridic', models.CharField(default=b'nopj', max_length=255, choices=[(b'pj', 'Filal\u0103'), (b'nopj', 'Sucursal\u0103'), (b'gi', 'Grup de ini\u021biativ\u0103')])),
                ('statut_drepturi', models.CharField(default=b'depline', max_length=255, choices=[(b'depline', b'Depline'), (b'suspendat', b'Suspendat'), (b'propus_desfiintare', 'Propus spre desfiin\u021bare'), (b'gi', b'Grup de ini\xc8\x9biativ\xc4\x83')])),
                ('preferinte_corespondenta', models.CharField(default=b'email', help_text='Asigura\u021bi-v\u0103 c\u0103 a\u021bi ad\u0103ugat informa\u021biile relevante de contact pentru tipul de coresponden\u021b\u0103 ales.', max_length=255, verbose_name='Preferin\u021b\u0103 trimitere coresponden\u021b\u0103', choices=[(b'email', b'Email'), (b'posta', 'Po\u0219t\u0103')])),
                ('logo', models.ImageField(null=True, upload_to=structuri.models.upload_to_centru_local_logo, blank=True)),
                ('antet', models.ImageField(null=True, upload_to=structuri.models.upload_to_centru_local_antent, blank=True)),
                ('moment_initial_cotizatie', models.ForeignKey(blank=True, to='documente.Trimestru', null=True)),
            ],
            options={
                'verbose_name': 'Centru Local',
                'verbose_name_plural': 'Centre Locale',
                'permissions': ('list_centrulocal', 'Poate vedea o list\u0103 cu Centrele lui Locale'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EtapaProgres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('ordine', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('slug', models.SlugField()),
                ('reguli', models.CharField(max_length=1024, null=True, blank=True)),
                ('logo', models.ForeignKey(to='album.Imagine')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EtapaProgresMembru',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField()),
                ('detalii', models.TextField(null=True, blank=True)),
                ('etapa_progres', models.ForeignKey(to='structuri.EtapaProgres')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagineProfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=photologue.models.get_storage_path, max_length=1024, verbose_name='image')),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, editable=False, blank=True)),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count', editable=False)),
                ('crop_from', models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center'), (b'auto', 'Auto (Default)')])),
                ('effect', models.ForeignKey(related_name='imagineprofil_related', verbose_name='effect', blank=True, to='photologue.PhotoEffect', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InformatieContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valoare', models.CharField(max_length=1024)),
                ('data_start', models.DateTimeField(null=True, blank=True)),
                ('data_end', models.DateTimeField(null=True, blank=True)),
                ('implicita', models.BooleanField(default=True)),
                ('object_id', models.PositiveIntegerField()),
                ('obiect_ref_id', models.PositiveIntegerField(null=True, blank=True)),
                ('informatii_suplimentare', models.CharField(max_length=1024, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('obiect_ref_ctype', models.ForeignKey(related_name='referit', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotaTargetEtapaProgres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('target_atins', models.BooleanField(default=False)),
                ('activitate', models.ForeignKey(blank=True, to='album.Eveniment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoteObiectivProgresMembru',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nota', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('obiectiv_atins', models.BooleanField(default=False)),
                ('activitate', models.ForeignKey(blank=True, to='album.Eveniment', null=True)),
                ('etapa_progres', models.ForeignKey(to='structuri.EtapaProgres')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ObiectivEducativProgres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titlu', models.CharField(max_length=2048)),
                ('descriere', models.TextField(null=True, blank=True)),
                ('domeniu', models.CharField(max_length=255, choices=[(b'intelectual', b'Intelectual'), (b'fizic', b'Fizic'), (b'afectiv', b'Afectiv'), (b'social', b'Social'), (b'caracter', b'Caracter'), (b'spiritual', b'Spiritual')])),
                ('pista', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patrula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('data_infiintare', models.DateField(null=True, blank=True)),
                ('activa', models.BooleanField(default=True)),
                ('moment_inchidere', models.DateField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Patrul\u0103',
                'verbose_name_plural': 'Patrule',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersoanaDeContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255, null=True, blank=True)),
                ('telefon', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('implicit', models.BooleanField(default=False)),
                ('job', models.CharField(max_length=255, null=True, verbose_name='Profesie, loc de munc\u0103', blank=True)),
                ('note', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RamuraDeVarsta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, null=True, blank=True)),
                ('varsta_intrare', models.PositiveSmallIntegerField()),
                ('varsta_iesire', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('culoare', models.CharField(max_length=255, null=True, blank=True)),
                ('are_patrule', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TargetEtapaProgres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titlu', models.CharField(max_length=2048)),
                ('capitol', models.CharField(max_length=2048)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipAsociereMembruStructura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('content_types', models.ManyToManyField(to='contenttypes.ContentType', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipInformatieContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('template_name', models.CharField(max_length=255, null=True, blank=True)),
                ('descriere', models.CharField(max_length=255, null=True, blank=True)),
                ('relevanta', models.CharField(max_length=255, null=True, blank=True)),
                ('adresa', models.BooleanField(default=False)),
                ('is_sms_capable', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipRelatieFamilie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('reverse_relationship', models.ForeignKey(blank=True, to='structuri.TipRelatieFamilie', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unitate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('data_infiintare', models.DateField(null=True, blank=True)),
                ('activa', models.BooleanField(default=True)),
                ('centru_local', models.ForeignKey(to='structuri.CentruLocal')),
                ('ramura_de_varsta', models.ForeignKey(to='structuri.RamuraDeVarsta')),
            ],
            options={
                'verbose_name': 'Unitate',
                'verbose_name_plural': 'Unit\u0103\u021bi',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Utilizator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('nume', models.CharField(max_length=255)),
                ('prenume', models.CharField(max_length=255)),
                ('hash', models.CharField(max_length=32, unique=True, null=True, blank=True)),
                ('timestamp_registered', models.DateTimeField(null=True, blank=True)),
                ('timestamp_confirmed', models.DateTimeField(null=True, blank=True)),
                ('timestamp_accepted', models.DateTimeField(null=True, blank=True)),
                ('requested_password_reset', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membru',
            fields=[
                ('utilizator_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='structuri.Utilizator')),
                ('cnp', models.CharField(max_length=255, unique=True, null=True, verbose_name='CNP', blank=True)),
                ('telefon', models.CharField(max_length=10, null=True, blank=True)),
                ('adresa', models.CharField(max_length=2048, null=True, blank=True)),
                ('data_nasterii', models.DateField(null=True, blank=True)),
                ('sex', models.CharField(blank=True, max_length=1, null=True, choices=[(b'm', 'Masculin'), (b'f', b'Feminin')])),
                ('scout_id', models.CharField(max_length=255, null=True, verbose_name=b'ID ONCR', blank=True)),
                ('scor_credit', models.IntegerField(default=2, help_text='Aceast\u0103 valoare reprezint\u0103 \xeencrederea Centrului Local \xeentr-un membru de a-\u0219i respecta angajamentele financiare (dac\u0103 Centrul are sau nu \xeencredere s\u0103 pun\u0103 bani pentru el / ea)', verbose_name='Credit', choices=[(0, 'R\u0103u'), (1, 'Neutru'), (2, 'Bun')])),
                ('familie', models.ManyToManyField(to='structuri.Membru', null=True, through='structuri.AsociereMembruFamilie', blank=True)),
                ('poza_profil', models.ForeignKey(blank=True, to='structuri.ImagineProfil', null=True)),
            ],
            options={
            },
            bases=('structuri.utilizator',),
        ),
        migrations.AddField(
            model_name='utilizator',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persoanadecontact',
            name='membru',
            field=models.ForeignKey(to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persoanadecontact',
            name='tip_relatie',
            field=models.ForeignKey(blank=True, to='structuri.TipRelatieFamilie', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patrula',
            name='unitate',
            field=models.ForeignKey(to='structuri.Unitate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noteobiectivprogresmembru',
            name='evaluator',
            field=models.ForeignKey(related_name='note_obiective_progres_evaluate', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noteobiectivprogresmembru',
            name='membru',
            field=models.ForeignKey(related_name='note_obiective_progres', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noteobiectivprogresmembru',
            name='obiectiv',
            field=models.ForeignKey(to='structuri.ObiectivEducativProgres'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notatargetetapaprogres',
            name='evaluator',
            field=models.ForeignKey(related_name='note_etape_progres_evaluate', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notatargetetapaprogres',
            name='membru',
            field=models.ForeignKey(related_name='note_etape_progres', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notatargetetapaprogres',
            name='target',
            field=models.ForeignKey(to='structuri.TargetEtapaProgres'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='informatiecontact',
            name='tip_informatie',
            field=models.ForeignKey(to='structuri.TipInformatieContact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='etapaprogresmembru',
            name='evaluator',
            field=models.ForeignKey(related_name='etape_progres_evaluate', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='etapaprogresmembru',
            name='membru',
            field=models.ForeignKey(related_name='etape_progres', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='etapaprogres',
            name='ramura_de_varsta',
            field=models.ForeignKey(to='structuri.RamuraDeVarsta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badgemeritmembru',
            name='evaluator',
            field=models.ForeignKey(related_name='badgeuri_merit_evaluate', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badgemeritmembru',
            name='membru',
            field=models.ForeignKey(related_name='badgeuri_merit', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badgemerit',
            name='etapa_progres',
            field=models.ForeignKey(blank=True, to='structuri.EtapaProgres', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badgemerit',
            name='logo',
            field=models.ForeignKey(blank=True, to='album.Imagine', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badgemerit',
            name='ramura_de_varsta',
            field=models.ForeignKey(blank=True, to='structuri.RamuraDeVarsta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrustructura',
            name='confirmata_de',
            field=models.ForeignKey(related_name='asocieri_confirmate', blank=True, to='structuri.Utilizator', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrustructura',
            name='content_type',
            field=models.ForeignKey(verbose_name='Tip structur\u0103', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrustructura',
            name='membru',
            field=models.ForeignKey(related_name='afilieri', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrustructura',
            name='tip_asociere',
            field=models.ForeignKey(to='structuri.TipAsociereMembruStructura'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrufamilie',
            name='persoana_destinatie',
            field=models.ForeignKey(related_name='membru_destinatie', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrufamilie',
            name='persoana_sursa',
            field=models.ForeignKey(to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asocieremembrufamilie',
            name='tip_relatie',
            field=models.ForeignKey(to='structuri.TipRelatieFamilie'),
            preserve_default=True,
        ),
    ]
