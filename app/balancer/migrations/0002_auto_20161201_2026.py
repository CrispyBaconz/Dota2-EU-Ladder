# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-01 17:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0005_auto_20161130_1348'),
        ('balancer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', jsonfield.fields.JSONField()),
                ('match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ladder.Match')),
            ],
        ),
        migrations.RemoveField(
            model_name='balanceresult',
            name='answers',
        ),
        migrations.AddField(
            model_name='balanceanswer',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balancer.BalanceResult'),
        ),
    ]