# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anon',
            name='title',
            field=models.CharField(default='Attention', max_length=200),
        ),
    ]
