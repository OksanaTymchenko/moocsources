# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-17 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0007_course_duration_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
