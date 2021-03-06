# Generated by Django 3.2.8 on 2022-03-10 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISP_warehouse', '0008_auto_20220310_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='image',
            field=models.ImageField(blank=True, default='static/warehouse/media/noimg.png', null=True, upload_to='static/warehouse/media/'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 14, 35, 24, 253135)),
        ),
    ]
