#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.db import models
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Person(models.Model):
    name = models.CharField(_('Nombre'), max_length=255, primary_key=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'person'
        verbose_name = 'person'
        verbose_name_plural = 'persons'
        ordering = ('name', )


    def __unicode__(self):
        return self.name
