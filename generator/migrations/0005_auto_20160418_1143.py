# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_auto_20160418_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='id',
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.TextField(default='All', primary_key=True, serialize=False),
        ),
    ]