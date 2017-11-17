# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 20:37
from __future__ import unicode_literals

from django.db import migrations, models
import questions.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_user_rating'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', questions.models.MyUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(default='static/ava.png', upload_to='uploads/%Y/%m/%d/'),
        ),
    ]