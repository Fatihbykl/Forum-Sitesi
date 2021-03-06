# Generated by Django 2.2.3 on 2019-10-30 21:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0010_auto_20191030_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(choices=[(1, 'Yeni Tim Üyesi'), (2, 'Kıdemli Tim Üyesi'), (3, 'Özel Tim Üyesi'), (4, 'Moderatör'), (5, 'Büro Destek'), (6, 'Admin')], default=1)),
                ('point', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='point',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 10, 31, 0, 46, 16, 583100)),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_rank',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userApp.Ranks'),
        ),
    ]
