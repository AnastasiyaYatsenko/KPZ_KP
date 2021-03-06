# Generated by Django 3.2.8 on 2022-03-10 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISP_warehouse', '0006_auto_20220310_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='image',
        ),
        migrations.AddField(
            model_name='inventory',
            name='image',
            field=models.ImageField(blank=True, default='./images/noimg.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 14, 22, 46, 395569)),
        ),
    ]
