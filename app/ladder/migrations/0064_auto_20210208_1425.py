# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-02-08 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0063_laddersettings_dota_lobby_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laddersettings',
            name='dota_lobby_name',
            field=models.CharField(default='RD2L', max_length=200),
        ),
    ]