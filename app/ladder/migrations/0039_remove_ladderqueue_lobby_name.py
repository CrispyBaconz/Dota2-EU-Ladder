# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-09-07 14:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0038_auto_20200907_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ladderqueue',
            name='lobby_name',
        ),
    ]