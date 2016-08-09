# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pipeline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorialModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(editable=False, max_length=50, null=True)),
                ('expected_runtime', models.IntegerField(default=0)),
                ('resources_ram_mb', models.IntegerField(default=2000, help_text=b'Amount of RAM (M) to be allocated for the AviJob')),
                ('resources_cpu_cores', models.IntegerField(default=1, help_text=b'Number of CPU cores to be allocated to the AviJob')),
                ('fib_num', models.IntegerField()),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tutorialmodel_model', to='pipeline.AviJobRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]