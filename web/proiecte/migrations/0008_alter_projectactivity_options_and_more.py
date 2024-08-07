# Generated by Django 4.1.7 on 2023-09-19 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proiecte', '0007_projectactivity_project_projectobjective_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectactivity',
            options={'ordering': ['-date_start']},
        ),
        migrations.AddField(
            model_name='projectactivity',
            name='objectives',
            field=models.ManyToManyField(blank=True, to='proiecte.projectobjective'),
        ),
        migrations.AddField(
            model_name='projectrole',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proiecte.project'),
        ),
    ]
