# Generated by Django 3.2.1 on 2023-04-28 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_alter_game_publicid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.IntegerField(choices=[(1, 'Waiting'), (2, 'Countdown'), (3, 'Question'), (4, 'Answer'), (5, 'Leaderboard')], default=1),
        ),
    ]
