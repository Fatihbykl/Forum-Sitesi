# Generated by Django 2.2.3 on 2019-10-27 11:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 10, 27, 14, 42, 57, 616195)),
        ),
    ]