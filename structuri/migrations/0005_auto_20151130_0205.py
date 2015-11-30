# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0004_auto_20150314_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membru',
            name='familie',
            field=models.ManyToManyField(to='structuri.Membru', through='structuri.AsociereMembruFamilie', blank=True),
        ),
        migrations.AlterField(
            model_name='persoanadecontact',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tipasocieremembrustructura',
            name='content_types',
            field=models.ManyToManyField(to='contenttypes.ContentType', blank=True),
        ),
        migrations.AlterField(
            model_name='utilizator',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
