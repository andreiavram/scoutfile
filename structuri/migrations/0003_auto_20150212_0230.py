# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0002_auto_20150212_0229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='centrulocal',
            options={'verbose_name': 'Centru Local', 'verbose_name_plural': 'Centre Locale', 'permissions': (('list_centrulocal', 'Poate vedea o list\u0103 cu Centrele lui Locale'),)},
        ),
    ]
