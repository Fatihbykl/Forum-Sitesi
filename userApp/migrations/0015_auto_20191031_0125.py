# Generated by Django 2.2.3 on 2019-10-30 22:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0014_auto_20191031_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranks',
            name='delete_post_perm',
            field=models.BooleanField(default=0, verbose_name='Konu Silme'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 10, 31, 1, 25, 44, 87618)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_rank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_rank', to='userApp.Ranks'),
        ),
    ]