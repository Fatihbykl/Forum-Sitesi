# Generated by Django 2.2.3 on 2019-10-30 21:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0011_auto_20191031_0046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ranks',
            options={'verbose_name_plural': 'Rütbeler'},
        ),
        migrations.RemoveField(
            model_name='ranks',
            name='point',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='point',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 10, 31, 0, 48, 15, 993737)),
        ),
    ]
