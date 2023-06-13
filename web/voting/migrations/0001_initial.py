# Generated by Django 4.1.7 on 2023-06-13 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documente', '0007_platacotizatietrimestru_payment_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Propusă'), (1, 'Deschisă'), (2, 'Vot suspendat'), (3, 'Vot finalizat')], default=0)),
                ('created', models.DateTimeField()),
                ('source', models.PositiveSmallIntegerField(choices=[(1, 'Organic'), (2, 'Slack')], default=1)),
                ('voting_enabled', models.BooleanField(default=False)),
                ('voting_model', models.PositiveSmallIntegerField(choices=[(1, '50% + 1'), (2, '2 / 3')], default=1)),
                ('quorum_model', models.PositiveSmallIntegerField(choices=[(1, '50% + 1'), (2, '2 / 3')], default=1)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TopicGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField()),
                ('datetime_end', models.DateTimeField()),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='VotingOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('motion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='voting.topic')),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='sessions',
            field=models.ManyToManyField(blank=True, to='voting.topicgroup'),
        ),
        migrations.CreateModel(
            name='DiscussionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('source', models.PositiveSmallIntegerField(default=1, verbose_name=[(1, 'Organic'), (2, 'Email'), (3, 'Slack')])),
                ('external_id', models.CharField(blank=True, max_length=255, null=True)),
                ('documents', models.ManyToManyField(blank=True, to='documente.document')),
                ('parent_topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='voting.discussionitem')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='voting.votingoptions')),
            ],
        ),
    ]
