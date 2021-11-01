# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('credit', models.IntegerField()),
                ('epuizat', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comentarii', models.TextField(null=True, blank=True)),
                ('tip', models.CharField(max_length=2, choices=[(1, b'Real'), (2, b'Intern')])),
                ('content_type', models.ForeignKey(verbose_name=b'Clas\xc4\x83', blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('creat_de', models.ForeignKey(blank=True, to='structuri.Utilizator', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RezervareCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=django.db.models.deletion.CASCADE)),
                ('credit', models.ForeignKey(to='patrocle.Credit', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('destinatar', models.CharField(max_length=1024)),
                ('mesaj', models.CharField(max_length=1024, null=True, blank=True)),
                ('cod_referinta_smslink', models.IntegerField()),
                ('timestamp_trimitere', models.DateTimeField(null=True, blank=True)),
                ('timestamp_confirmare', models.DateTimeField(null=True, blank=True)),
                ('confirmat', models.BooleanField(default=False)),
                ('eroare_trimitere', models.CharField(max_length=1024, null=True, blank=True)),
                ('eroare_confirmare', models.CharField(max_length=1024, null=True, blank=True)),
                ('sender', models.CharField(max_length=255, null=True, blank=True)),
                ('cod_grup', models.CharField(max_length=255, null=True, blank=True)),
                ('credit', models.ForeignKey(blank=True, to='patrocle.Credit', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('expeditor', models.ForeignKey(to='structuri.Utilizator', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
