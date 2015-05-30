#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.db import models
from django.utils.translation import ugettext as _

from jsonfield import JSONField
from vld.objects import Ingredient as VldIngredient

from ingredient.helper import process_ingredients

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Recipe(models.Model):
    name = models.CharField(_('Nombre'), max_length=255, unique=True)
    ingredients = JSONField()
    amount = models.FloatField(_('Cantidad'))
    unit = models.CharField(_('Unidad'), max_length=30)
    data = JSONField()

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        db_table = 'recipe'
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def as_object(self):
        return VldIngredient.from_json(self.data)

    def save(self, *args, **kwargs):
        ingredient = VldIngredient(
            name=self.name,
            sample_size=self.amount,
            sample_unit=self.unit,
            sample_value=process_ingredients(self.ingredients).nutritional_value)
        self.data = ingredient.as_json()
        super(Recipe, self).save(*args, **kwargs)

    @classmethod
    def all_objects(cls):
        return [r.as_object() for r in cls.objects.all()]

    def get_absolute_url(self):
        return reverse('ingredient:recipe_detail', kwargs={'recipe_id': self.id})

    def __unicode__(self):
        return self.name
