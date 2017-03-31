# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import scoutfile3.s3utils
import documente


class Migration(migrations.Migration):

    dependencies = [
        ('documente', '0003_auto_20150314_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='fisier',
            field=models.FileField(storage=scoutfile3.s3utils.LocalStorage(), null=True, upload_to=documente.models.upload_to_document_fisier, blank=True),
            preserve_default=True,
        ),
    ]
