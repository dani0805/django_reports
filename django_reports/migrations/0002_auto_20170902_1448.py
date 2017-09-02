# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='description',
            field=models.CharField(default='-', max_length=500, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='style',
            field=models.CharField(default='pie', max_length=10, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.CharField(default='-', max_length=100, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(unique=True, max_length=10, verbose_name='Name'),
        ),
    ]
