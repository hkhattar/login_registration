# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 23:29
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_auto_20161020_2316'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('userManager', django.db.models.manager.Manager()),
            ],
        ),
    ]
