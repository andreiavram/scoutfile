# Generated by Django 4.1.7 on 2023-07-15 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0021_migrate_external_albums'),
    ]

    operations = [
        migrations.AddField(
            model_name='camparbitrarparticipareeveniment',
            name='user_fillable',
            field=models.BooleanField(default=False),
        ),
    ]
