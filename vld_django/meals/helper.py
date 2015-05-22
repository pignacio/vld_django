#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from var_log_dieta.commands.report import process_log
from var_log_dieta.ingredient import IngredientMap

from ingredient.models import Ingredient

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def process_meal_data(meal):
    ingredients = IngredientMap([x.as_object()
                                 for x in Ingredient.objects.all()])
    return process_log(meal.date.strftime('%F'), meal.data, ingredients)
