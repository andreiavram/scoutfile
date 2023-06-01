# Generated by Django 4.1.7 on 2023-02-21 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0013_alter_photo_image_alter_watermark_image'),
        ('album', '0008_auto_20211031_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagine',
            name='effect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='photologue.photoeffect', verbose_name='effect'),
        ),
        migrations.AlterField(
            model_name='participareeveniment',
            name='status_participare',
            field=models.IntegerField(choices=[(1, 'Cu semnul întrebării'), (2, 'Confirmat'), (3, 'Avans plătit'), (4, 'Participare efectivă'), (6, 'Participare efectivă (online)'), (7, 'Participare efectivă (fizic)'), (5, 'Participare anulată')], default=1),
        ),
    ]
