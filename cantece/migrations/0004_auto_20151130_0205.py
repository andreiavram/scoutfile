# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cantece', '0003_auto_20150330_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartecantece',
            name='optiuni_template',
            field=models.ManyToManyField(to='cantece.OptiuniTemplateCarteCantece', blank=True),
        ),
    ]
