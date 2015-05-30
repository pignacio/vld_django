#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-many-ancestors
from __future__ import absolute_import, unicode_literals, division

import json
import logging

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView

from ingredient.helper import get_ingredients_data
from utils.views import LoginRequiredMixin

from .models import Recipe
from .forms import RecipeForm

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:list')

    def get_context_data(self, *args, **kwargs):
        data = super(RecipeCreateView, self).get_context_data(*args, **kwargs)
        data['title'] = _('Agregar receta')
        data['ingredients'] = json.dumps(get_ingredients_data(), indent=1)
        return data


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    pk_url_kwarg = 'recipe_id'
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:list')

    def get_context_data(self, *args, **kwargs):
        data = super(RecipeUpdateView, self).get_context_data(*args, **kwargs)
        data['title'] = _('Editar receta')
        data['ingredients'] = json.dumps(get_ingredients_data(), indent=1)
        return data
