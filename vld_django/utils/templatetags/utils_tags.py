#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django import template
from django.core.urlresolvers import resolve, Resolver404

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

register = template.Library()  # pylint: disable=invalid-name


@register.simple_tag
def active_page(request, view_name, text='active'):
    resolved = _resolve_request_path(request)
    if resolved and resolved.url_name == view_name:
        return text
    return ''


@register.simple_tag
def active_namespace(request, namespace, text='active'):
    resolved = _resolve_request_path(request)
    if resolved and namespace in resolved.namespaces:
        return text
    return ''


def _resolve_request_path(request):
    if not request:
        return None
    try:
        return resolve(request.path_info)
    except Resolver404:
        return None


_STATUSES = ['none', 'ok', 'warning', 'danger']


@register.filter(name='range_class')
def range_class(value, value_range, warning=10):
    if value_range is None or value is None:
        return 'none'
    status_id = 0
    if value_range.lower is not None:
        if value < value_range.lower * (100 - warning) / 100:
            status_id = max(status_id, 3)
        elif value < value_range.lower:
            status_id = max(status_id, 2)
        else:
            status_id = max(status_id, 1)
    if value_range.upper is not None:
        if value < value_range.upper:
            status_id = max(status_id, 1)
        elif value < value_range.upper * (100 + warning) / 100:
            status_id = max(status_id, 2)
        else:
            status_id = max(status_id, 3)

    return _STATUSES[status_id]


@register.filter
def range_string(value_range):
    if value_range is None:
        return ''
    lower, upper = value_range.lower, value_range.upper
    if lower is None:
        return '' if upper is None else "<{}".format(upper)
    else:
        return '>{}'.format(lower) if upper is None else "{}-{}".format(lower, upper)
