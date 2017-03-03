# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0004_auto_20150314_1335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participareeveniment',
            options={'ordering': ['-data_sosire', 'status_participare']},
        ),
    ]
