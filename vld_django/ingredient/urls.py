#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals, division

import logging

from django.conf.urls import patterns, url

from . import views

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

urlpatterns = patterns(  # pylint: disable=invalid-name
    'ingredient.views',
    url(r'^list$', views.IngredientListView.as_view(), name='list'),
    url(r'^create$', views.IngredientCreateView.as_view(), name='create'),
    url(r'^import$', views.IngredientMassImportView.as_view(), name='import'),
    url(r'^detail/(?P<ingredient_id>\d+)$', views.IngredientDetailView.as_view(), name='detail'),
    url(r'^finder$', views.ingredient_finder, name='finder'),
)  # yapf: disable
