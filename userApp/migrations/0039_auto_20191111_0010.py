# Generated by Django 2.2.3 on 2019-11-10 21:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0038_auto_20191108_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 11, 11, 0, 10, 16, 439044)),
        ),
    ]
