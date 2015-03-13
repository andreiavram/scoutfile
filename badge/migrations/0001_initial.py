# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_auto_20150212_0220'),
        ('structuri', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nume', models.CharField(max_length=255)),
                ('descriere', models.CharField(max_length=2048, null=True, blank=True)),
                ('tip', models.CharField(max_length=255, choices=[(b'eveniment', 'Eveniment'), (b'progres', 'Progres'), (b'merit', 'Merit'), (b'altul', 'Alt tip de badge')])),
                ('tiraj', models.IntegerField()),
                ('tiraj_exact', models.BooleanField(default=False, help_text='Tirajul este cunoscut exact')),
                ('producator', models.CharField(help_text='Unde a fost produs badge-ul?', max_length=255, null=True, blank=True)),
                ('designer', models.CharField(max_length=255, null=True, blank=True)),
                ('data_productie', models.DateField()),
                ('status', models.CharField(default=b'produs', max_length=255)),
                ('disponibil_in', models.TextField(help_text='Unde poate fi g\u0103sit badge-ul, c\xe2te o loca\u021bie pe linie', null=True, verbose_name='Unde se poate g\u0103si', blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('designer_membru', models.ForeignKey(blank=True, to='structuri.Membru', null=True)),
                ('owner', models.ForeignKey(related_name='badgeuri', to='structuri.Membru')),
                ('poza_badge', models.ForeignKey(blank=True, to='album.Imagine', null=True)),
            ],
            options={
                'ordering': ['-data_productie'],
            },
            bases=(models.Model,),
        ),
    ]
