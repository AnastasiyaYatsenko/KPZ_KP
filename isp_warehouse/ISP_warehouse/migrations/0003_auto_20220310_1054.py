# Generated by Django 3.2.8 on 2022-03-10 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISP_warehouse', '0002_auto_20220310_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='document',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 10, 54, 54, 507056)),
        ),
        migrations.AlterField(
            model_name='operation',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
