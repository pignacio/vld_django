#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from jsonfield import JSONField

from .helper import process_meal

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Meal(models.Model):
    person = models.ForeignKey('persons.Person')
    date = models.DateField(_('Fecha'))
    data = JSONField()
    is_free = models.BooleanField(_('Es día libre?'), default=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'meal'
        verbose_name = 'meal'
        verbose_name_plural = 'meals'
        unique_together = ('person', 'date', )
        ordering = ('person', 'date', )

    def get_absolute_url(self):
        return reverse('meals:detail', kwargs={'person_name': self.person.name, 'date': self.date})

    def __unicode__(self):
        return "{}@{}".format(self.person, self.date)

    def log(self):
        return process_meal(self)


class MealPhoto(models.Model):
    image = models.ImageField(upload_to='meals.MealPhotoData/bytes/filename/mimetype')
    meal = models.ForeignKey(Meal, related_name='photos')
    path = models.CharField(max_length=255, db_index=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'meal_screenshot'
        verbose_name = 'meal screenshot'
        verbose_name_plural = 'meal screenshots'
        ordering = ('path', )


class MealPhotoData(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)
