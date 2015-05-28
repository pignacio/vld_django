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
        yield make_chart(chart_definition, date_start, date_end, person.values, logs)


def make_chart(chart_def, start, end, values, logs):
    options = {
        'width': 900,
        'height': 500,
        'axes': {
            'y': {}
        },
        'series': {
        }
    }  # yapf: disable

    columns = [('string', 'Date')]

    for i, value_def in enumerate(chart_def['values']):
        axis = value_def['axis']
        options['axes']['y'][axis] = {'label': axis}
        options['series'][i] = {'axis': axis}
        columns.append(('number', value_def['value']))

    rows = []
    date = start
    while date <= end:
        date_str = date.strftime('%F')
        row = [date_str]
        for value_def in chart_def['values']:
            value_name = value_def['value']
            if value_name.startswith('meal:'):
                attr = value_name[5:]
                try:
                    value = getattr(logs[date_str].nutritional_value, attr)
                except KeyError:
                    value = None
            else:
                value = values.get(value_name, {}).get(date_str, None)
            row.append(value)
        rows.append(row)
        date += datetime.timedelta(days=1)

    return Chart(columns, rows, options)
