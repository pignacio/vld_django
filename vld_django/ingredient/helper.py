#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from vld.commands.report import process_log
from vld.ingredient import IngredientMap


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def all_ingredients():
    from .models import Ingredient
    from recipes.models import Recipe
    return Ingredient.all_objects() + Recipe.all_objects()


def process_ingredients(ingredients):
    ingredient_map = IngredientMap(all_ingredients())
    return process_log('Ingredient', {'__init__': ingredients}, ingredient_map)


def get_ingredients_data():
    ingredients = [{'name': i.name, 'units': _get_units(i)} for i in all_ingredients()]
    return ingredients


def _get_units(ingredient):
    units = ingredient.valid_units(ingredient.sample_unit)
    values = ["{} ({:.2f} {})".format(unit, amount, ingredient.sample_unit) if
              unit != ingredient.sample_unit else unit for unit, amount in units.items()]
    return ", ".join(values)
