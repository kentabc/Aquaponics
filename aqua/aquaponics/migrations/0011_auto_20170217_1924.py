# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-17 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquaponics', '0010_auto_20170212_2108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant_type',
            old_name='name',
            new_name='plant_name',
        ),
        migrations.AlterField(
            model_name='fish',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plant',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
