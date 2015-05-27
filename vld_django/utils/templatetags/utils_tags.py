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


@register.filter(name='range_class')
def range_class(value, value_range, warning=10):
    if value_range is None or value is None:
        return 'none'
    if value < value_range.lower * (100 - warning) / 100:
        return 'danger'
    elif value < value_range.lower:
        return 'warning'
    elif value < value_range.upper:
        return 'ok'
    elif value < value_range.upper * (100 + warning) / 100:
        return 'warning'
    else:
        return 'danger'
