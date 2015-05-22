# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Fecha')),
                ('data', jsonfield.fields.JSONField(default=dict)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
            options={
                'ordering': ('person', 'date'),
                'db_table': 'meal',
                'verbose_name': 'meal',
                'verbose_name_plural': 'meals',
            },
        ),
        migrations.AlterUniqueTogether(
            name='meal',
            unique_together=set([('person', 'date')]),
        ),
    ]
