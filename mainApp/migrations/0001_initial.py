# Generated by Django 2.2.3 on 2019-11-06 12:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('comment_text', models.TextField(max_length=2000)),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_quote', to='mainApp.Comments')),
            ],
            options={
                'verbose_name_plural': 'Yorumlar',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=75)),
                ('name', models.CharField(max_length=70, null=True)),
                ('topic', models.CharField(max_length=120)),
                ('text', models.TextField(max_length=3000)),
            ],
            options={
                'verbose_name_plural': 'İletişim',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=1, max_length=50)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Alt Kategoriler',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(max_length=5000)),
                ('created_time', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 12, 13, 56, 264461, tzinfo=utc))),
                ('slug', models.SlugField(editable=False, max_length=150)),
                ('is_fixed', models.BooleanField(default=0)),
                ('is_locked', models.BooleanField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategory', to='mainApp.SubCategory')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Gönderiler',
            },
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 12, 13, 56, 265491, tzinfo=utc))),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='mainApp.Post')),
                ('who_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Gönderi Beğenileri',
            },
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime(2019, 11, 6, 12, 13, 56, 265491, tzinfo=utc))),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='mainApp.Comments')),
                ('who_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_like_com', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Yorum Beğenileri',
            },
        ),
        migrations.AddField(
            model_name='comments',
            name='which_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='which_post', to='mainApp.Post'),
        ),
        migrations.AddField(
            model_name='comments',
            name='who_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=1, max_length=50)),
                ('slug', models.SlugField()),
                ('sub_category', models.ManyToManyField(related_name='sub_category', to='mainApp.SubCategory')),
            ],
            options={
                'verbose_name_plural': 'Kategoriler',
            },
        ),
    ]