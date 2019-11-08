# Generated by Django 2.2.3 on 2019-10-30 21:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0013_auto_20191031_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranks',
            name='category_perm',
            field=models.BooleanField(default=0, verbose_name='Kategori Açma/Kapama'),
        ),
        migrations.AddField(
            model_name='ranks',
            name='color_text_perm',
            field=models.BooleanField(default=0, verbose_name='Renkli Yazı'),
        ),
        migrations.AddField(
            model_name='ranks',
            name='delete_user_perm',
            field=models.BooleanField(default=0, verbose_name='Üye Silme'),
        ),
        migrations.AddField(
            model_name='ranks',
            name='edit_comments_perm',
            field=models.BooleanField(default=0, verbose_name='Mesaj Düzenleme (Başkasının)'),
        ),
        migrations.AddField(
            model_name='ranks',
            name='pin_perm',
            field=models.BooleanField(default=0, verbose_name='Konu Sabitleme'),
        ),
        migrations.AddField(
            model_name='ranks',
            name='post_lock_perm',
            field=models.BooleanField(default=0, verbose_name='Konu Kilitleme/Açma'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2019, 10, 31, 0, 59, 21, 561684)),
        ),
    ]
