#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import datetime
import logging

from django.contrib.postgres.fields import FloatRangeField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from annoying.fields import AutoOneToOneField
from jsonfield import JSONField
import pytz

from meals.helper import process_meals

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Person(models.Model):
    name = models.CharField(_('Nombre'), max_length=255, primary_key=True)
    owner = models.OneToOneField('auth.User', null=True, blank=True)
    default_meal_data = JSONField(_('Comida por defecto'))
    valid_calories = FloatRangeField(_('Calorías válidas'), null=True, blank=True)
    valid_carbs = FloatRangeField(_('Carbs válidos'), null=True, blank=True)
    valid_proteins = FloatRangeField(_('Proteínas válidas'), null=True, blank=True)
    valid_fat = FloatRangeField(_('Grasas válidas'), null=True, blank=True)
    valid_fiber = FloatRangeField(_('Fibra válida'), null=True, blank=True)
    timezone = models.CharField(_('Timezone'),
                                choices=[(tz, tz) for tz in pytz.all_timezones],
                                max_length=255, default='UTC')
    values = JSONField(_('Valores'), default={})
    charts = JSONField(_('Gráficos'), default=[])

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
        if today not in by_date:
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
        now = datetime.datetime.now()
        utc_now = pytz.utc.localize(now)
        tz_now = utc_now.astimezone(pytz.timezone(self.timezone))
        return tz_now.date()


class UserProfile(models.Model):
    user = AutoOneToOneField('auth.User', primary_key=True, related_name='profile')

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'user_profile'
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    def __unicode__(self):
        return "Profile for {}".format(self.user)

    def visible_persons(self):
        return Person.objects.all()
