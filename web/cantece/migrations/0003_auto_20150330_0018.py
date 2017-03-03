# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import scoutfile3.s3utils
from web import cantece


class Migration(migrations.Migration):

    dependencies = [
        ('cantece', '0002_auto_20150314_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatecartecantece',
            name='template_file',
            field=models.FileField(storage=scoutfile3.s3utils.LocalStorage(), upload_to=cantece.models.upload_to_template_carte_cantece),
            preserve_default=True,
        ),
    ]
