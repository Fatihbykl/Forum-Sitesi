# Generated by Django 2.2.3 on 2019-11-07 19:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20191107_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likecomment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 19, 23, 51, 529915, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 19, 23, 51, 529915, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 19, 23, 51, 528918, tzinfo=utc)),
        ),
    ]
