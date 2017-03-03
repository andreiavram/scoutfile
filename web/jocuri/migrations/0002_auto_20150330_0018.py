# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jocuri', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fisaactivitate',
            name='tags',
            field=jocuri.models.FixedTaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
