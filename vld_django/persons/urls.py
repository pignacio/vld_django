#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals, division

import logging

from django.conf.urls import patterns, url

from . import views

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

urlpatterns = patterns(  # pylint: disable=invalid-name
    'persons.views',
    url(r'^$', views.PersonListView.as_view(), name='list'),
    url(r'^create$', views.PersonCreateView.as_view(), name='create'),
    url(r'^(?P<person_name>\w+)/import$', views.PersonImportView.as_view(), name='import'),
    url(r'^(?P<person_name>\w+)/update$', views.PersonUpdateView.as_view(), name='update'),
    url(r'^(?P<person_name>\w+)$', views.PersonDetailView.as_view(), name='detail'),
    url(r'^(?P<person_name>\w+)/values$', views.PersonValuesView.as_view(), name='values'),
    url(r'^(?P<person_name>\w+)/values/create$', views.PersonCreateValueView.as_view(), name='create_value'),
    url(r'^(?P<person_name>\w+)/values/select_date$', views.PersonValuesSelectDatesView.as_view(), name='select_date'),
    url(r'^(?P<person_name>\w+)/values/add/(?P<date_start>\d{4}-\d{2}-\d{2})/(?P<date_end>\d{4}-\d{2}-\d{2})$', views.PersonAddValuesView.as_view(), name='add_values'),
)  # yapf: disable
