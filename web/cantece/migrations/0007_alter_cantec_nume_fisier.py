# Generated by Django 4.1.7 on 2023-07-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cantece', '0006_alter_cantec_nume_fisier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cantec',
            name='nume_fisier',
            field=models.FilePathField(verbose_name='/home/yeti/PycharmProjects/scoutfile/media/cartecantece/cantece'),
        ),
    ]