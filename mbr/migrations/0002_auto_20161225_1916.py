# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flighttable',
            name='level270',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='flighttable',
            name='level320',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='flighttable',
            name='level360',
            field=models.BooleanField(default=False),
        ),
    ]