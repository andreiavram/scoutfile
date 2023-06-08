# Generated by Django 4.1.7 on 2023-06-08 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0014_alter_imagine_effect_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('required', 'Necesar pentru participare la'), ('offered', 'Oferit de')], max_length=255)),
                ('limited_for_role', models.CharField(choices=[('participant', 'Participant'), ('insotitor', 'Lider însoțitor'), ('invitat', 'Invitat'), ('coordonator', 'Coordonator'), ('staff', 'Membru staff')], max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='status',
            field=models.CharField(blank=True, choices=[('propus', 'Propus'), ('confirmat', 'Confirmat'), ('derulare', 'În derulare'), ('terminat', 'Încheiat'), ('anulat', 'Anulat')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='tip_eveniment_text',
            field=models.CharField(blank=True, choices=[('camp', 'Camp'), ('intalnire', 'Întâlnire'), ('intalnire_unitate', 'Întâlnire unitate'), ('intalnire_patrula', 'Întâlnire patrulă'), ('intalnire_organizare', 'Întâlnire organizare'), ('hike', 'Hike'), ('social', 'Proiect social'), ('comunitate', 'Proiect de implicare în comunitate'), ('citychallange', 'City Challange'), ('international', 'Proiect internațional'), ('festival', 'Festival'), ('ecologic', 'Proiect ecologic'), ('training', 'Stagiu / training'), ('alta', 'Alt tip de eveniment')], default='alta', max_length=255, null=True),
        )
    ]
