# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-17 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0006_course_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration_filter',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
