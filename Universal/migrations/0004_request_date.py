# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-27 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Universal', '0003_user_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
