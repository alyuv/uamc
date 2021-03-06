# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 00:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mbr', '0005_auto_20161229_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='MbrLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiondate', models.DateTimeField(default=django.utils.timezone.now)),
                ('operation', models.CharField(max_length=50)),
                ('result', models.TextField()),
                ('request', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mbr_log',
            },
        ),
    ]
