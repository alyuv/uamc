# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbr', '0006_mbrlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='flighttable',
            name='number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
