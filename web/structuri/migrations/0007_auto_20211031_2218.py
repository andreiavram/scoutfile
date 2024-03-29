# Generated by Django 2.0 on 2021-10-31 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0006_tipinformatiecontact_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgemerit',
            name='etapa_progres',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='structuri.EtapaProgres'),
        ),
        migrations.AlterField(
            model_name='badgemerit',
            name='ramura_de_varsta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='structuri.RamuraDeVarsta'),
        ),
        migrations.AlterField(
            model_name='centrulocal',
            name='preferinte_corespondenta',
            field=models.CharField(choices=[('email', 'Email'), ('posta', 'Poștă')], default='email', help_text='Asigurați-vă că ați adăugat informațiile relevante de contact pentru tipul de corespondență ales.', max_length=255, verbose_name='Preferință trimitere corespondență'),
        ),
        migrations.AlterField(
            model_name='centrulocal',
            name='specific',
            field=models.CharField(blank=True, choices=[('catolic', 'Catolic'), ('marinaresc', 'Marinăresc')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='centrulocal',
            name='statut_drepturi',
            field=models.CharField(choices=[('depline', 'Depline'), ('suspendat', 'Suspendat'), ('propus_desfiintare', 'Propus spre desființare'), ('gi', 'Grup de inițiativă')], default='depline', max_length=255),
        ),
        migrations.AlterField(
            model_name='centrulocal',
            name='statut_juridic',
            field=models.CharField(choices=[('pj', 'Filală'), ('nopj', 'Sucursală'), ('gi', 'Grup de inițiativă')], default='nopj', max_length=255),
        ),
        migrations.AlterField(
            model_name='etapaprogres',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='album.Imagine'),
        ),
        migrations.AlterField(
            model_name='imagineprofil',
            name='crop_from',
            field=models.CharField(blank=True, choices=[('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left'), ('center', 'Center (Default)')], default='center', max_length=10, verbose_name='crop from'),
        ),
        migrations.AlterField(
            model_name='imagineprofil',
            name='date_taken',
            field=models.DateTimeField(blank=True, help_text='Date image was taken; is obtained from the image EXIF data.', null=True, verbose_name='date taken'),
        ),
        migrations.AlterField(
            model_name='membru',
            name='scout_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID ONCR'),
        ),
        migrations.AlterField(
            model_name='membru',
            name='sex',
            field=models.CharField(blank=True, choices=[('m', 'Masculin'), ('f', 'Feminin')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='obiectiveducativprogres',
            name='domeniu',
            field=models.CharField(choices=[('intelectual', 'Intelectual'), ('fizic', 'Fizic'), ('afectiv', 'Afectiv'), ('social', 'Social'), ('caracter', 'Caracter'), ('spiritual', 'Spiritual')], max_length=255),
        ),
        migrations.AlterField(
            model_name='persoanadecontact',
            name='tip_relatie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='structuri.TipRelatieFamilie'),
        ),
        migrations.AlterField(
            model_name='tipinformatiecontact',
            name='categorie',
            field=models.CharField(default='Contact', max_length=255),
        ),
    ]
