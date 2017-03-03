# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0005_auto_20150330_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='setpoze',
            name='default_visibility_level',
            field=models.IntegerField(default=-1, null=True, blank=True, choices=[(1, b'Secret'), (2, b'Centru Local'), (3, b'Organiza\xc8\x9bie'), (4, b'Public')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='setpoze',
            name='offset_secunde',
            field=models.IntegerField(default=0, help_text='Num\u0103rul de secunde cu care ceasul camerei voastre a fost decalat fa\u021b\u0103 de ceasul corect (poate fi \u0219i negativ). Foarte util pentru sincronizarea pozelor de la mai mul\u021bi fotografi'),
            preserve_default=True,
        ),
    ]
