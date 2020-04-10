# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-03 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaponics', '0031_auto_20171203_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testing',
            name='amonia',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='testing',
            name='nitrate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='testing',
            name='nitrite',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='testing',
            name='ph',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=5, null=True),
        ),
    ]
