# Generated by Django 3.2.8 on 2022-03-09 14:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='')),
                ('serial_num', models.TextField()),
                ('cost', models.IntegerField()),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LocType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.category')),
            ],
        ),
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 3, 9, 14, 13, 17, 809092))),
                ('notes', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='ISP_warehouse.location')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='ISP_warehouse.location')),
                ('from_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_place', to='ISP_warehouse.location')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.inventory')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='loc_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.loctype'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.location'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.supplier'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.type'),
        ),
    ]
