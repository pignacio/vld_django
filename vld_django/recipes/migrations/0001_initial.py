# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Nombre')),
                ('ingredients', jsonfield.fields.JSONField(default=dict)),
                ('amount', models.FloatField(verbose_name='Cantidad')),
                ('unit', models.CharField(max_length=30, verbose_name='Unidad')),
                ('data', jsonfield.fields.JSONField(default=dict)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'recipe',
                'verbose_name': 'recipe',
                'verbose_name_plural': 'recipes',
            },
        ),
    ]
