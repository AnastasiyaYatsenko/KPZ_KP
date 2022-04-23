# Generated by Django 3.2.8 on 2022-04-19 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISP_warehouse', '0015_auto_20220419_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='document',
            field=models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 19, 15, 8, 47, 944041)),
        ),
    ]
