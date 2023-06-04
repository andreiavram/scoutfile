# Generated by Django 4.1.7 on 2023-06-04 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financiar', '0006_alter_bankstatementitem_unique_together'),
        ('album', '0010_trackeveniment_programeveniment'),
    ]

    operations = [
        migrations.AddField(
            model_name='eveniment',
            name='frecventa',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eveniment',
            name='instanta_anterioara',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_occurrences', to='album.eveniment'),
        ),
        migrations.AddField(
            model_name='eveniment',
            name='instanta_urmatoare',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_occurrences', to='album.eveniment'),
        ),
        migrations.AddField(
            model_name='eveniment',
            name='instante_extra',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='participareeveniment',
            name='contribution_payments',
            field=models.ManyToManyField(related_name='payments', to='financiar.paymentdocument'),
        ),
        migrations.AlterField(
            model_name='participareeveniment',
            name='status_participare',
            field=models.IntegerField(choices=[(1, 'Cu semnul întrebării'), (2, 'Confirmat'), (3, 'Avans plătit'), (4, 'Participare efectivă'), (6, 'Participare efectivă (online)'), (7, 'Participare efectivă (fizic)'), (5, 'Participare anulată')], default=1),
        ),
        migrations.CreateModel(
            name='EventContributionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('description', models.TextField()),
                ('is_default', models.BooleanField(default=False)),
                ('config', models.JSONField(default=dict)),
                ('per_diem', models.BooleanField(default=False)),
                ('eveniment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contribution_options', to='album.eveniment')),
            ],
        ),
        migrations.AddField(
            model_name='participareeveniment',
            name='contribution_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='album.eventcontributionoption'),
        ),
    ]
