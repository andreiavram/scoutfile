# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0001_initial'),
        ('proiecte', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskitemresponsibility',
            name='owner',
            field=models.ForeignKey(related_name='task_associations', to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskitemresponsibility',
            name='target',
            field=models.ForeignKey(to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskitem',
            name='owner',
            field=models.ForeignKey(blank=True, to='structuri.Membru', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskitem',
            name='parent_task',
            field=models.ForeignKey(blank=True, to='proiecte.TaskItem', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectposition',
            name='member',
            field=models.ForeignKey(to='structuri.Membru'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectposition',
            name='project',
            field=models.ForeignKey(to='proiecte.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectposition',
            name='role',
            field=models.ForeignKey(to='proiecte.ProjectRole'),
            preserve_default=True,
        ),
    ]
