# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_auto_20150212_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='eveniment',
            name='oncr_id',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagine',
            name='crop_from',
            field=models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center (Default)')]),
            preserve_default=True,
        ),
    ]
