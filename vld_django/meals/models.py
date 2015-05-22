#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from jsonfield import JSONField

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Meal(models.Model):
    person = models.ForeignKey('persons.Person')
    date = models.DateField(_('Fecha'))
    data = JSONField()

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'meal'
        verbose_name = 'meal'
        verbose_name_plural = 'meals'
        unique_together = ('person', 'date', )
        ordering = ('person', 'date', )

    def get_absolute_url(self):
        return reverse(
            'meals:detail',
            kwargs={'person_name': self.person.name,
                    'date': self.date})

    def __unicode__(self):
        return "{}@{}".format(self.person, self.date)
