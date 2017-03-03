# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0003_auto_20150212_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagineprofil',
            name='crop_from',
            field=models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center (Default)')]),
            preserve_default=True,
        ),
    ]
