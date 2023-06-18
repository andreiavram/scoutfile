# Generated by Django 4.1.7 on 2023-06-01 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structuri', '0008_echipa'),
        ('inventar', '0002_auto_20211031_2218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='obiectinventar',
            old_name='multi_part',
            new_name='is_multi_part',
        ),
        migrations.RenameField(
            model_name='obiectinventar',
            old_name='denumire',
            new_name='titlu',
        ),
        migrations.AddField(
            model_name='locatieinventar',
            name='adresa_fizica',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locatieinventar',
            name='imagine',
            field=models.ImageField(blank=True, null=True, upload_to='inventar/locuri/'),
        ),
        migrations.AddField(
            model_name='obiectinventar',
            name='imagine',
            field=models.ImageField(blank=True, null=True, upload_to='inventar/obiect/'),
        ),
        migrations.AddField(
            model_name='obiectinventar',
            name='is_container',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='obiectinventar',
            name='cod_inventar',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='obiectinventar',
            name='responsabil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='structuri.membru'),
        ),
        migrations.AlterField(
            model_name='obiectinventar',
            name='stare',
            field=models.CharField(choices=[('nou', 'Nou'), ('fb', 'Foarte bună'), ('b', 'Bună'), ('u', 'Utilizabil'), ('r', 'Are nevoie de reparații'), ('p', 'Proastă'), ('d', 'De aruncat')], max_length=255),
        ),
        migrations.CreateModel(
            name='RelatieObiecteInventar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip_relatie', models.CharField(blank=True, choices=[('part_of', 'face parte din'), ('has_part', 'are în componență'), ('stored_in', 'este înmagazinat în'), ('stores', 'este container pentru'), ('tool_for', 'este necesar pentru mentenanța'), ('needs_tool', 'are nevoie pentru mentenanță de')], max_length=255, null=True)),
                ('obiect_inventar_sursa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='inventar.obiectinventar')),
                ('obiect_inventar_tinta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='inventar.obiectinventar')),
            ],
        ),
        migrations.CreateModel(
            name='MentenantaObiectInventar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titlu', models.CharField(max_length=255)),
                ('descriere', models.TextField()),
                ('perioada', models.DurationField()),
                ('obiect_inventar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventar.obiectinventar')),
            ],
        ),
        migrations.CreateModel(
            name='ExecutieMentenantaObiectInventar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planificata_pentru', models.DateTimeField(blank=True, null=True)),
                ('executata_la', models.DateTimeField(blank=True, null=True)),
                ('executata_de', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structuri.membru')),
                ('mentenanta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventar.mentenantaobiectinventar')),
            ],
        ),
    ]