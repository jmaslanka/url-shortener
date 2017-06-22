# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grivurl',
            name='shortcode',
            field=models.CharField(default='defaultvalue', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grivurl',
            name='url',
            field=models.CharField(max_length=254),
        ),
    ]
