# Generated by Django 2.2.6 on 2019-10-24 11:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191024_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 24, 11, 49, 47, 122804, tzinfo=utc), verbose_name='创建时间'),
        ),
    ]
