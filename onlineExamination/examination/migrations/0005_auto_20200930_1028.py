# Generated by Django 3.1.1 on 2020-09-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0004_auto_20200930_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
    ]
