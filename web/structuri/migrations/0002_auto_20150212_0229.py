# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='centrulocal',
            options={'verbose_name': 'Centru Local', 'verbose_name_plural': 'Centre Locale'},
        ),
    ]
