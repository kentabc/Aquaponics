# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-12 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaponics', '0007_auto_20170212_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fish',
            name='crop',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='plant',
            name='crop',
            field=models.CharField(max_length=15),
        ),
    ]
