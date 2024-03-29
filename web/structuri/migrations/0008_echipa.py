# Generated by Django 3.2.15 on 2022-09-20 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0007_auto_20211031_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Echipa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=255)),
                ('data_infiintare', models.DateField(blank=True, null=True)),
                ('activa', models.BooleanField(default=True)),
                ('centru_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='echipe', to='structuri.centrulocal')),
            ],
            options={
                'verbose_name': 'Echipă',
                'verbose_name_plural': 'Echipe',
            },
        ),
    ]
