# Generated by Django 4.1.7 on 2023-07-07 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0016_utilizator_porecla'),
    ]

    operations = [
        migrations.AddField(
            model_name='asocieremembrufamilie',
            name='end_date',
            field=models.DateField(blank=True, help_text='Pentru relații care încetează după obținerea calității de membru', null=True, verbose_name='Data sfârșit'),
        ),
        migrations.AddField(
            model_name='asocieremembrufamilie',
            name='start_date',
            field=models.DateField(blank=True, help_text='Pentru relații care intervin după obținerea calității de membru', null=True, verbose_name='Data început'),
        ),
        migrations.AlterField(
            model_name='utilizator',
            name='porecla',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]