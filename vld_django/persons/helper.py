#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import collections
import datetime
import logging

from meals.helper import process_meals

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# pylint: disable=invalid-name
Chart = collections.namedtuple('Chart', ['columns', 'rows', 'options'])


def make_charts(person, date_start, date_end):
    meals = person.meal_set.filter(date__gte=date_start, date__lte=date_end)
    logs = {m.date.strftime('%F'): l for m, l in process_meals(meals)}
    for chart_definition in person.charts:
        yield make_chart(chart_definition, date_start, date_end, person, logs)


def make_chart(chart_def, start, end, person, logs):
    options = {
        'width': 900,
        'height': 500,
        'interpolateNulls': True,
        'vAxes': {
        },
        'series': {
        }
    }  # yapf: disable

    vAxes = []

    columns = [('string', 'Date')]

    for i, value_def in enumerate(chart_def['values']):
        axis = value_def['axis']
        if axis not in vAxes:
            vAxes.append(axis)
        index = vAxes.index(axis)

        options['vAxes'][index] = {'title': axis, }
        options['series'][i] = {'targetAxisIndex': index}
        if value_def['value'].startswith(_LIMIT_VALUE_PREFIX):
            options['series'][i]['lineDashStyle'] = [5, 3]
        columns.append(('number', value_def['value']))

    rows = []
    date = start
    while date <= end:
        date_str = date.strftime('%F')
        row = [date_str]
        for value_def in chart_def['values']:
            try:
                value = _get_value(value_def['value'], date_str, person, logs.get(date_str, None))
            except Exception:  # pylint: disable=broad-except
                logger.debug("Problems extracting value for '%s'@%s", value_def, date_str,
                             exc_info=True)
                value = None

            row.append(round(value, 1) if value else value)
        rows.append(row)
        date += datetime.timedelta(days=1)

    return Chart(columns, rows, options)


def _get_value(value_name, date_str, person, meal_log):
    if value_name.startswith(_MEAL_VALUE_PREFIX):
        return _get_meal_value(value_name[len(_MEAL_VALUE_PREFIX):], meal_log)
    elif value_name.startswith(_LIMIT_VALUE_PREFIX):
        return _get_limit_value(value_name[len(_LIMIT_VALUE_PREFIX):], person)
    elif value_name.startswith(_DIFF_VALUE_PREFIX):
        return _get_diff_value(value_name[len(_DIFF_VALUE_PREFIX):], date_str, person)
    else:
        return person.values.get(value_name, {}).get(date_str, None)


def _get_meal_value(attr, log):
    return getattr(log.nutritional_value, attr) if log else 0


def _get_limit_value(limit_def, person):
    name, limit = limit_def.split(':', 1)
    attr = 'valid_' + name
    limit_range = getattr(person, attr)
    return getattr(limit_range, limit) if limit_range else None


def _get_diff_value(diff_def, date_str, person):
    value_name, diff = diff_def.split(":", 1)
    diff = int(diff)
    values = person.values.get(value_name, {})
    try:
        current = values[date_str]
    except KeyError:
        return None

    cur_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    for delta in [0, 1, -1]:
        date = cur_date - datetime.timedelta(days=delta + diff)
        try:
            date_value = values[date.strftime("%F")]
        except KeyError:
            pass
        else:
            return current - date_value

    return None


_LIMIT_VALUE_PREFIX = 'limit:'
_MEAL_VALUE_PREFIX = 'meal:'
_DIFF_VALUE_PREFIX = 'diff:'
