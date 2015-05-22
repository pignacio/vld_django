#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import (ListView, DetailView, UpdateView,
                                  CreateView)

from utils.views import LoginRequiredMixin
from meals.models import Meal
from meals.helper import trim_meals_data
from .models import Person
from .forms import PersonImportForm

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ('name', )
    template_name = 'persons/person_create.html'

    def get_success_url(self):
        return reverse('persons:detail',
                       kwargs={'person_name': self.object.name})


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    pk_url_kwarg = 'person_name'


class PersonImportView(LoginRequiredMixin, UpdateView):
    model = Person
    pk_url_kwarg = 'person_name'
    form_class = PersonImportForm
    template_name_suffix = '_import'

    def form_valid(self, form):
        for date, data in form.cleaned_data['data'].items():
            try:
                meal = self.object.meal_set.get(date=date)
            except Meal.DoesNotExist:
                meal = Meal(person=self.object, date=date)
            meal.data = trim_meals_data(data)
            meal.save()

        return redirect(self.object.get_absolute_url())




class PersonListView(LoginRequiredMixin, ListView):
    model = Person
