# Generated by Django 3.2.1 on 2023-04-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_auto_20230402_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.IntegerField(choices=[(1, 'Waiting'), (2, 'Question'), (3, 'Answer'), (4, 'Leaderboard')], default=1),
        ),
    ]