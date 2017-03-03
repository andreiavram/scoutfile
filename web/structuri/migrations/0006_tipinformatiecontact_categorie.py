# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0005_auto_20151130_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipinformatiecontact',
            name='categorie',
            field=models.CharField(default=b'Contact', max_length=255),
        ),
    ]
