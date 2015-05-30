#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals, division

import logging

from django.conf.urls import patterns, url

from . import views

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

urlpatterns = patterns(  # pylint: disable=invalid-name
    'meals.views',
    url(r'^(?P<person_name>\w+)/create$', views.MealCreateView.as_view(), name='create'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})$', views.MealDetailView.as_view(), name='detail'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/add/(?P<path>.*)$', views.MealAddSectionView.as_view(), name='add_section'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/edit/(?P<path>.*)$', views.MealEditSectionView.as_view(), name='edit_section'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/delete/(?P<path>.*)$', views.MealAddSectionView.as_view(), name='delete_section'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/toggle_free$', views.meal_toggle_free, name='toggle_free'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<path>.*)/create_photo$', views.MealCreatePhotoView.as_view(), name='create_photo'),
    url(r'^(?P<person_name>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<path>.*)/counter$', views.meal_counter, name='counter'),
)  # yapf: disable
