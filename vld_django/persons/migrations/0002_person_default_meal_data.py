# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='default_meal_data',
            field=jsonfield.fields.JSONField(default=dict, verbose_name='Comida por defecto'),
        ),
    ]
