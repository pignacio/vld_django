#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from unidecode import unidecode
from var_log_dieta.commands.report import process_log
from var_log_dieta.ingredient import IngredientMap

from ingredient.models import Ingredient

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def process_meal(meal):
    return process_meal_data(meal.date.strftime('%F'), meal.data)


def process_meal_data(name, data):
    ingredients = IngredientMap([x.as_object()
                                 for x in Ingredient.objects.all()])
    return process_log(name, data, ingredients)


def trim_meals_data(data):
    res = {}

    for key, value in data.items():
        if key == '__init__':
            if not value:
                continue
            trimmed = value
        else:
            trimmed = trim_meals_data(value)
            if not trimmed:
                continue
        res[key] = trimmed
    return res


def get_ingredients_data():
    ingredients = [i.as_object() for i in Ingredient.objects.all()]
    ingredients = [{'name': unidecode(i.name),
                    'units': _get_units(i)} for i in ingredients]
    return ingredients


def _get_units(ingredient):
    units = ingredient.valid_units(ingredient.sample_unit)
    values = ["{} ({:.2f} {})".format(unit, amount, ingredient.sample_unit)
              if unit != ingredient.sample_unit else unit
              for unit, amount in units.items()]
    return ", ".join(values)
