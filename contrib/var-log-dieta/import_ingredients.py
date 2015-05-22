#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import json
import logging
import os

from var_log_dieta.objects import Ingredient, NutritionalValue

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _extract_columns(line):
    split = line.rstrip('\n').split('\t')
    return split[:1] + split[4:]


def _get_value(field):
    return float(field) if field else None


def main():
    with open('ingredients.tsv') as fin:
        lines = fin.readlines()

    headers = _extract_columns(lines[0])
    ingredients_data = [_extract_columns(l) for l in lines[1:]]

    ingredients = []

    for data in ingredients_data:
        values = zip(headers, data)
        nut_value = NutritionalValue(
            **{k: _get_value(v)
               for k, v in values[3:]})
        ingredient_values = dict(values[:3])
        ingredient_values['sample_size'] = float(
            ingredient_values['sample_size'])
        ingredients.append(Ingredient(sample_value=nut_value,
                                      **ingredient_values))

    root_dir = '/tmp/ingredients'
    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)
    for ingredient in ingredients:
        fname = os.path.join(root_dir, ingredient.name.replace('/', ''))
        with open(fname, 'w') as fout:
            json.dump([ingredient.as_json()], fout, indent=1)


if __name__ == '__main__':
    main()
