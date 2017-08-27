# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-27 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_courseorg_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='student_nums',
            field=models.IntegerField(default=0, verbose_name='学生人数'),
        ),
    ]
