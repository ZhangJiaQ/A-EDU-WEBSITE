# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-27 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_teacher_years_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=20, verbose_name='标签'),
        ),
    ]
