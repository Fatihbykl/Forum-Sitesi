# Generated by Django 2.2.3 on 2019-11-27 13:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0045_auto_20191127_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 11, 27, 16, 27, 21, 520090)),
        ),
    ]