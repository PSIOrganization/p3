# Generated by Django 3.2.1 on 2023-03-31 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=5000)),
                ('correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation')),
                ('state', models.IntegerField(choices=[(1, 'Waiting'), (2, 'Question'), (3, 'Answer'), (4, 'Leaderboard')])),
                ('publicId', models.IntegerField(unique=True)),
                ('countdownTime', models.IntegerField()),
                ('questionNo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last-update')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last-update')),
                ('answerTime', models.IntegerField()),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=20)),
                ('points', models.IntegerField(default=0)),
                ('uuidP', models.UUIDField(default=uuid.uuid4)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.game')),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.answer')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.game')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.participant')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.question')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.questionnaire'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.question'),
        ),
    ]
