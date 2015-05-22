#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,too-many-ancestors
from __future__ import absolute_import, unicode_literals, division

import logging

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, FormView

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

    def get_success_url(self):
        return reverse('ingredient:detail',
                       ingredient_id=self.object.id)


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient/ingredient_create.html'

    def get_success_url(self):
        return reverse('ingredient:detail',
                       kwargs={'ingredient_id': self.object.id})


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


