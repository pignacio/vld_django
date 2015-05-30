#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals, division

import logging

from django.conf.urls import patterns, url

from . import views

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'recipes.views',
    url(r'^list$', views.RecipeListView.as_view(), name='list'),
    url(r'^create$', views.RecipeCreateView.as_view(), name='create'),
    url(r'^update/(?P<recipe_id>\d+)$', views.RecipeUpdateView.as_view(), name='update'),
)  # yapf: disable
