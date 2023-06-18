# Generated by Django 4.1.7 on 2023-06-01 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proiecte', '0005_projectobjective_taskitem_completed_and_more'),
        ('financiar', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('structuri', '0008_echipa'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentdocument',
            name='project_budget_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proiecte.projectbudgetentry'),
        ),
        migrations.AddField(
            model_name='paymentdocument',
            name='project_budget_line',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proiecte.projectbudgetline'),
        ),
        migrations.AddField(
            model_name='paymentdocument',
            name='registered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentdocument',
            name='third_party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financiar.legalentity'),
        ),
        migrations.AddField(
            model_name='bankstatementitem',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financiar.bankstatement'),
        ),
        migrations.AddField(
            model_name='bankstatement',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financiar.bankaccount'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='centru_local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structuri.centrulocal'),
        ),
    ]