# Generated by Django 2.0 on 2021-10-31 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0007_auto_20151130_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camparbitrarparticipareeveniment',
            name='tip_camp',
            field=models.CharField(choices=[('text', 'Text'), ('number', 'Număr'), ('bool', 'Bifă'), ('date', 'Dată')], max_length=255),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='custom_cover_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='album.Imagine'),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='proiect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proiecte.Project'),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='published_status',
            field=models.IntegerField(choices=[(1, 'Secret'), (2, 'Centru Local'), (3, 'Organizație'), (4, 'Public')], default=2, verbose_name='Vizibilitate'),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='responsabil_articol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evenimente_articol', to='structuri.Membru'),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='responsabil_raport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evenimente_raport', to='structuri.Membru'),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='status',
            field=models.CharField(blank=True, choices=[('propus', 'Propus'), ('confirmat', 'Confirmat'), ('derulare', 'În derulare'), ('terminat', 'Încheiat')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='eveniment',
            name='tip_eveniment_text',
            field=models.CharField(blank=True, choices=[('camp', 'Camp'), ('intalnire', 'Întâlnire'), ('hike', 'Hike'), ('social', 'Proiect social'), ('comunitate', 'Proiect de implicare în comunitate'), ('citychallange', 'City Challange'), ('international', 'Proiect internațional'), ('festival', 'Festival'), ('ecologic', 'Proiect ecologic'), ('alta', 'Alt tip de eveniment'), ('training', 'Stagiu / training')], default='alta', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='flagreport',
            name='motiv',
            field=models.CharField(choices=[('personal', 'Sunt în poză și nu sunt de acord să apară aici'), ('ofensa', 'Consider că poza este ofensatoare'), ('nonscout', 'Poza conține un comportament necercetășesc și nu ar trebui listată aici'), ('calitateslaba', 'Poza este de calitate slabă și nu merită păstrată'), ('altul', 'Alt motiv')], max_length=1024),
        ),
        migrations.AlterField(
            model_name='imagine',
            name='crop_from',
            field=models.CharField(blank=True, choices=[('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left'), ('center', 'Center (Default)')], default='center', max_length=10, verbose_name='crop from'),
        ),
        migrations.AlterField(
            model_name='imagine',
            name='date_taken',
            field=models.DateTimeField(blank=True, help_text='Date image was taken; is obtained from the image EXIF data.', null=True, verbose_name='date taken'),
        ),
        migrations.AlterField(
            model_name='imagine',
            name='effect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagine_related', to='photologue.PhotoEffect', verbose_name='effect'),
        ),
        migrations.AlterField(
            model_name='imagine',
            name='published_status',
            field=models.IntegerField(choices=[(1, 'Secret'), (2, 'Centru Local'), (3, 'Organizație'), (4, 'Public')], default=2, verbose_name='Vizibilitate'),
        ),
        migrations.AlterField(
            model_name='participareeveniment',
            name='nonmembru',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='album.ParticipantEveniment'),
        ),
        migrations.AlterField(
            model_name='participareeveniment',
            name='rol',
            field=models.CharField(choices=[('participant', 'Participant'), ('insotitor', 'Lider însoțitor'), ('invitat', 'Invitat'), ('coordonator', 'Coordonator'), ('staff', 'Membru staff')], default='participant', max_length=255),
        ),
        migrations.AlterField(
            model_name='raporteveniment',
            name='accept_publicare_raport_national',
            field=models.BooleanField(default=True, help_text='Dacă se propune această activitate pentru raportul anual al ONCR', verbose_name='Acord raport ONCR'),
        ),
        migrations.AlterField(
            model_name='setpoze',
            name='default_visibility_level',
            field=models.IntegerField(blank=True, choices=[(1, 'Secret'), (2, 'Centru Local'), (3, 'Organizație'), (4, 'Public')], default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='setpoze',
            name='status',
            field=models.IntegerField(choices=[(0, 'Initialized'), (1, 'Zip Uploaded'), (2, 'Zip queued for processing'), (3, 'Zip processed OK'), (4, 'Zip error')], default=0),
        ),
        migrations.AlterField(
            model_name='setpoze',
            name='zip_file',
            field=models.FilePathField(blank=True, null=True, path='/tmp'),
        ),
    ]
