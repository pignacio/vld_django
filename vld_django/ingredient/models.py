#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.db import models
from django.utils.translation import ugettext as _

from jsonfield import JSONField
from var_log_dieta.objects import Ingredient as VldIngredient

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Ingredient(models.Model):
    name = models.CharField(_('Nombre'), max_length=255, unique=True)
    data = JSONField()

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'ingredient'
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'

    def as_object(self):
        return VldIngredient.from_json(self.data)

    def save_as(self, ingredient):
        self.name = ingredient.name
        self.data = ingredient.as_json()
        self.save()
