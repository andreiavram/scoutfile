# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20150314_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='raporteveniment',
            name='altele',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='aventura',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='cultural',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='ecologie',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='fundraising',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='social',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raporteveniment',
            name='spiritual',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
