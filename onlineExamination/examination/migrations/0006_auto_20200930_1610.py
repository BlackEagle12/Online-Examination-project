# Generated by Django 3.1.1 on 2020-09-30 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0005_auto_20200930_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='obtained_marks',
            field=models.IntegerField(),
        ),
    ]
