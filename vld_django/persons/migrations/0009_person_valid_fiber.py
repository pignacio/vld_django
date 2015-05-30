# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0008_person_charts'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='valid_fiber',
            field=django.contrib.postgres.fields.ranges.FloatRangeField(null=True, verbose_name='Fibra v\xe1lida', blank=True),
        ),
    ]
