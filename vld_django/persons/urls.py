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
    url(r'^(?P<person_name>\w+)$', views.PersonDetailView.as_view(), name='detail'),
)  # yapf: disable
