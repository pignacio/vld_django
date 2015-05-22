#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals, division

import logging

from django.conf.urls import patterns, url

from . import views

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

urlpatterns = patterns(  # pylint: disable=invalid-name
    'web.views',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login$', views.login, name='login'),
)  # yapf: disable
