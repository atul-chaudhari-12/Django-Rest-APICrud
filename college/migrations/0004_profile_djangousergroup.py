# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0003_remove_profile_studing_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='djangousergroup',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]