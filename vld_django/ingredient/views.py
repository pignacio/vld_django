#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,too-many-ancestors
from __future__ import absolute_import, unicode_literals, division

import logging

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView

from .forms import IngredientForm, IngredientImportForm
from .models import Ingredient

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Create your views here.


class IngredientListView(ListView):
    model = Ingredient


class IngredientImportView(CreateView):
    model = Ingredient
    form_class = IngredientImportForm
    template_name = 'ingredient/ingredient_import.html'

    def get_success_url(self):
        return reverse('ingredient:detail',
                       ingredient_id=self.form.instance.id)


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient/ingredient_create.html'

    def get_success_url(self):
        return reverse('ingredient:detail',
                       ingredient_id=self.form.instance.id)


class IngredientDetailView(DetailView):
    model = Ingredient
    pk_url_kwarg = 'ingredient_id'
