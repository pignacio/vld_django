# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_meal_is_free'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='meals.MealPhotoData/bytes/filename/mimetype')),
                ('path', models.CharField(max_length=255, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('meal', models.ForeignKey(related_name='photos', to='meals.Meal')),
            ],
            options={
                'ordering': ('path',),
                'db_table': 'meal_screenshot',
                'verbose_name': 'meal screenshot',
                'verbose_name_plural': 'meal screenshots',
            },
        ),
        migrations.CreateModel(
            name='MealPhotoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
    ]
