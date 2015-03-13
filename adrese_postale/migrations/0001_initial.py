# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodPostal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cod_postal', models.CharField(max_length=6)),
                ('judet', models.CharField(max_length=255)),
                ('localitate', models.CharField(max_length=255)),
                ('tip_strada', models.CharField(max_length=255, null=True, blank=True)),
                ('strada', models.CharField(max_length=255, null=True, blank=True)),
                ('sector', models.IntegerField(null=True, blank=True)),
                ('descriptor', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
