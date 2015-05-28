# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0007_person_values'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='charts',
            field=jsonfield.fields.JSONField(default=[], verbose_name='Gr\xe1ficos'),
        ),
    ]
