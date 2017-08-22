# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 14:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='end_date',
            field=models.DateField(default=datetime.date.today, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='start_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Start date'),
        ),
    ]
