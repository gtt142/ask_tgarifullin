# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20171116_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(default='img/ava.png', upload_to='%Y/%m/%d/'),
        ),
    ]
