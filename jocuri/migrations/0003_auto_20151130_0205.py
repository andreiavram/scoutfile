# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jocuri', '0002_auto_20150330_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fisaactivitate',
            name='ramuri_de_varsta',
            field=models.ManyToManyField(to='structuri.RamuraDeVarsta', blank=True),
        ),
    ]
