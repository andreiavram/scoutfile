# Generated by Django 4.1.7 on 2024-01-15 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicaltag',
            name='to_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]