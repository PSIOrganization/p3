# Generated by Django 3.2.1 on 2023-04-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_alter_question_answertime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='publicId',
            field=models.IntegerField(default=839302, unique=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='questionNo',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
