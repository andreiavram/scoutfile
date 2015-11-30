# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proiecte', '0002_auto_20150212_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstate',
            name='available_states',
            field=models.ManyToManyField(to='proiecte.TaskState', blank=True),
        ),
    ]
