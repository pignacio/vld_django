# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_person_valid_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='valid_carbs',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Carbs v\xe1lidos'),
        ),
        migrations.AddField(
            model_name='person',
            name='valid_fat',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Grasas v\xe1lidas'),
        ),
        migrations.AddField(
            model_name='person',
            name='valid_proteins',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Prote\xednas v\xe1lidas'),
        ),
    ]
