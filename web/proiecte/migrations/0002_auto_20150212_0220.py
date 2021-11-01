# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
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
            field=models.ForeignKey(related_name='task_associations', to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskitemresponsibility',
            name='target',
            field=models.ForeignKey(to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskitem',
            name='owner',
            field=models.ForeignKey(blank=True, to='structuri.Membru', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskitem',
            name='parent_task',
            field=models.ForeignKey(blank=True, to='proiecte.TaskItem', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectposition',
            name='member',
            field=models.ForeignKey(to='structuri.Membru', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectposition',
            name='project',
            field=models.ForeignKey(to='proiecte.Project', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectposition',
            name='role',
            field=models.ForeignKey(to='proiecte.ProjectRole', on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
    ]
