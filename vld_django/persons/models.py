#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import datetime
import logging

from django.contrib.postgres.fields import FloatRangeField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from jsonfield import JSONField

from meals.helper import process_meals

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Person(models.Model):
    name = models.CharField(_('Nombre'), max_length=255, primary_key=True)
    default_meal_data = JSONField(_('Comida por defecto'))
    valid_calories = FloatRangeField(_('Calorías válidas'), null=True, blank=True)
    valid_carbs = FloatRangeField(_('Carbs válidos'), null=True, blank=True)
    valid_proteins = FloatRangeField(_('Proteínas válidas'), null=True, blank=True)
    valid_fat = FloatRangeField(_('Grasas válidas'), null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'person'
        verbose_name = 'person'
        verbose_name_plural = 'persons'
        ordering = ('name', )

    def get_absolute_url(self):
        return reverse('persons:detail', kwargs={'person_name': self.name})

    def __unicode__(self):
        return self.name

    def _list_all_meals(self, start_date=None):
        model = self.meal_set.model
        meals = self.meal_set.all()
        if start_date:
            meals = meals.filter(date__gte=start_date)
        meals = meals.reverse()

        by_date = {m.date: m for m in meals}
        today = self.today_date()
        if not today in by_date:
            by_date[today] = model(person=self, date=today)

        start = max(by_date)
        end = min(by_date)
        date = start
        res = []
        while date >= end:
            res.append(by_date.get(date, model(person=self, date=date)))
            date -= datetime.timedelta(days=1)
        return res

    def processed_meals(self):
        meals = self._list_all_meals()
        return process_meals(meals)

    def today_date(self):
        return datetime.date.today()
