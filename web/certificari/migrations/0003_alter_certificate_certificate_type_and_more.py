# Generated by Django 4.1.7 on 2024-09-04 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0021_membru_data_initiala_cotizatie_and_more'),
        ('certificari', '0002_certificate_valid_until_certificationtype_validity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='certificate_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificari.certificationtype', verbose_name='Tip certificat'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='issued_by',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Emitent'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='issued_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificari', to='structuri.membru', verbose_name='Titluar'),
        ),
    ]
