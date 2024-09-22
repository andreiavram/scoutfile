# Generated by Django 4.1.7 on 2023-07-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financiar', '0007_bankstatementitem_notes_bankstatementitem_registered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdocument',
            name='document_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='document_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='document_type',
            field=models.CharField(choices=[('factura', 'Factura'), ('chitanta', 'Chitanta'), ('bon_fiscal', 'Bon Fiscal'), ('bilet', 'Bilet'), ('decont', 'Decont'), ('dispozitie_plata', 'Dispoziție de plată'), ('dispoziție_incasare', 'Dispoziție de încasare'), ('op', 'Ordin de plată'), ('other', 'Altele')], max_length=255, verbose_name='Tip înregistrare'),
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='internal_reference',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='notes',
            field=models.TextField(verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='value',
            field=models.FloatField(verbose_name='Valoare'),
        ),
    ]