# Generated by Django 2.2.3 on 2019-11-02 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0025_auto_20191102_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 11, 2, 18, 54, 40, 440019)),
        ),
    ]
