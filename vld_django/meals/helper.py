#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from unidecode import unidecode
from vld.commands.report import process_log
from vld.ingredient import IngredientMap

from ingredient.helper import all_ingredients

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def process_meal(meal):
    return process_meals([meal])[0][1]


def process_meals(meals):
    meals = list(meals)
    logs = process_meal_datas((meal.date.strftime('%F'), meal.data) for meal in meals)
    return zip(meals, logs)


def process_meal_data(name, data):
    return process_meal_datas([(name, data)])[0]


def process_meal_datas(datas):
    ingredients = IngredientMap(all_ingredients())
    return [process_log(name, data, ingredients) for name, data in datas]


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
