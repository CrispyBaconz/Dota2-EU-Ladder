# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0015_auto_20161227_1518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['rank_mmr']},
        ),
        migrations.RenameField(
            model_name='player',
            old_name='rank',
            new_name='rank_mmr',
        ),
    ]