# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_auto_20160422_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='options',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
