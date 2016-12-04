# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookfinder', '0003_auto_20161203_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='gid',
            field=models.CharField(default='NA', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='NA', max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('book', 'user_name')]),
        ),
    ]
