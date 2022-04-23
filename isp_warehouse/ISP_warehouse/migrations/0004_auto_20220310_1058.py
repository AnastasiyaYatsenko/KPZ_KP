# Generated by Django 3.2.8 on 2022-03-10 10:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISP_warehouse', '0003_auto_20220310_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='comment',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='document',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 10, 58, 0, 159018)),
        ),
        migrations.AlterField(
            model_name='operation',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='type',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
    ]