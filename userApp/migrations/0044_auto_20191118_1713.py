# Generated by Django 2.2.3 on 2019-11-18 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0043_auto_20191118_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 11, 18, 17, 12, 59, 954050)),
        ),
    ]