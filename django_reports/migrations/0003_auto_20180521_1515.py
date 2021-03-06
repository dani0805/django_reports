# Generated by Django 2.0.1 on 2018-05-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_reports', '0002_auto_20170902_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='report',
            name='source_code',
            field=models.TextField(max_length=60000, verbose_name='Source Code'),
        ),
    ]
