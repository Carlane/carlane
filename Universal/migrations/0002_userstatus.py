# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Universal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_status', models.CharField(max_length=50)),
            ],
        ),
    ]
