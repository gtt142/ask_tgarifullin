# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-18 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20171209_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='questions.Category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(default='static/img/ava.png', upload_to='%Y/%m/%d/', verbose_name='Аватар'),
        ),
    ]
