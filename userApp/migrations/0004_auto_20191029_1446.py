# Generated by Django 2.2.3 on 2019-10-29 11:46

import datetime
from django.db import migrations, models
import userApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0003_auto_20191028_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 10, 29, 14, 46, 8, 74423)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(upload_to=userApp.models.upload_to_directory),
        ),
    ]
