# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 06:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botform', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submissions',
            old_name='payload',
            new_name='data',
        ),
    ]
