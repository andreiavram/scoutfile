# Generated by Django 4.1.7 on 2024-04-02 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0020_membru_current_centru_local_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membru',
            name='data_initiala_cotizatie',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membru',
            name='scor_credit',
            field=models.IntegerField(choices=[(0, 'Rău'), (1, 'Neutru'), (2, 'Good')], default=2, help_text='Această valoare reprezintă încrederea Centrului Local într-un membru de a-și respecta angajamentele financiare (dacă Centrul are sau nu încredere să pună bani pentru el / ea)', verbose_name='Credit'),
        ),
    ]
