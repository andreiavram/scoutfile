# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0006_auto_20150330_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eveniment',
            name='oncr_id',
            field=models.CharField(max_length=255, null=True, verbose_name='ONCR ID', blank=True),
        ),
        migrations.AlterField(
            model_name='participanteveniment',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
