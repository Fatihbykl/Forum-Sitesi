# Generated by Django 2.2.3 on 2019-11-02 17:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0028_auto_20191102_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='timastamp',
            new_name='timestamp',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 11, 2, 20, 30, 15, 698074)),
        ),
    ]
