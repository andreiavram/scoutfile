# Generated by Django 4.1.7 on 2023-06-08 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proiecte', '0005_projectobjective_taskitem_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectbudgetentry',
            name='direction',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Income'), (2, 'Expediture')], default=2),
        ),
    ]