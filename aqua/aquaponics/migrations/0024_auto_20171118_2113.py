# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-19 01:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquaponics', '0023_auto_20171118_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquaponics.tasks'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
