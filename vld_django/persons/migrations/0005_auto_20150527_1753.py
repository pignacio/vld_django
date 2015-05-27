# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0004_auto_20150527_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='valid_calories',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Calor\xedas v\xe1lidas', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='valid_carbs',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Carbs v\xe1lidos', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='valid_fat',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Grasas v\xe1lidas', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='valid_proteins',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Prote\xednas v\xe1lidas', blank=True),
        ),
    ]
