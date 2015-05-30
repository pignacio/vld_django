# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0006_person_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='values',
            field=jsonfield.fields.JSONField(default={}, verbose_name='Valores'),
        ),
    ]
