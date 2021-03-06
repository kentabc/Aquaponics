# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-08-03 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquaponics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='fish_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fish_name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(max_length=15)),
                ('amount', models.IntegerField()),
                ('plant_date', models.DateField(verbose_name='Date Planted')),
                ('plant_time', models.TimeField(verbose_name='Time Planted')),
                ('comment', models.TextField(blank=True, null=True)),
                ('plant_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquaponics.plant_type')),
            ],
        ),
    ]
