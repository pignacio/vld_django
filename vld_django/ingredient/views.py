#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,too-many-ancestors
from __future__ import absolute_import, unicode_literals, division

import json
import logging

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, FormView

from unidecode import unidecode
from var_log_dieta.objects import Ingredient as VldIngredient

from utils.views import LoginRequiredMixin
from .forms import (IngredientForm, IngredientImportForm,
                    IngredientMassImportForm)
from .models import Ingredient

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Create your views here.


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient


class IngredientImportView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientImportForm
    template_name = 'ingredient/ingredient_import.html'
    success_url = reverse_lazy('ingredient:list')


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient/ingredient_create.html'
    success_url = reverse_lazy('ingredient:list')


class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    pk_url_kwarg = 'ingredient_id'


class IngredientMassImportView(LoginRequiredMixin, FormView):
    form_class = IngredientMassImportForm
    template_name = 'ingredient/ingredient_import.html'

    def form_valid(self, form):
        datas = form.cleaned_data['data']
        for data in datas:
            try:
                name = data["name"]
                try:
                    ingredient = Ingredient.objects.get(name=name)
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient()
                ingredient.save_as(VldIngredient.from_json(data))
            except Exception:
                logger.exception('Error importing ingredient from %s', data)
        return redirect('ingredient:list')


def _get_units(ingredient):
    units = ingredient.valid_units(ingredient.sample_unit)
    values = ["{} ({:.2f} {})".format(unit, amount, ingredient.sample_unit)
              if unit != ingredient.sample_unit else unit
              for unit, amount in units.items()]
    return ", ".join(values)


def ingredient_finder(request):
    ingredients = [i.as_object() for i in Ingredient.objects.all()]
    ingredients = [{'name': unidecode(i.name),
                    'units': _get_units(i)} for i in ingredients]
    return render(request, 'ingredient/finder.html',
                  {'ingredients': json.dumps(ingredients,
                                             indent=1)})
