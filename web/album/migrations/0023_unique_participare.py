# Generated by Django 4.1.7 on 2023-07-15 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0018_centrulocal_default_payment_domain_and_more'),
        ('album', '0022_camparbitrarparticipareeveniment_user_fillable_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participareeveniment',
            unique_together={('eveniment', 'membru')},
        ),
    ]
