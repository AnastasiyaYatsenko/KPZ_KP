# Generated by Django 3.2.8 on 2022-03-10 10:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ISP_warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 3, 10, 10, 26, 53, 829959))),
                ('notes', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='ISP_warehouse.location')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='ISP_warehouse.location')),
                ('from_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_place', to='ISP_warehouse.location')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISP_warehouse.inventory')),
            ],
        ),
        migrations.DeleteModel(
            name='Operations',
        ),
    ]
