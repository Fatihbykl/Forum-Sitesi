# Generated by Django 2.2.3 on 2019-11-03 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0030_auto_20191103_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 11, 3, 14, 53, 51, 134570)),
        ),
    ]
