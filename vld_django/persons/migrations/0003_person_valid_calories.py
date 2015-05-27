# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_person_default_meal_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='valid_calories',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Calor\xedas v\xe1lidas'),
        ),
    ]
