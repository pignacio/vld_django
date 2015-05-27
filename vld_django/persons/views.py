#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from utils.views import LoginRequiredMixin
from meals.models import Meal
from meals.helper import trim_meals_data
from .models import Person
from .forms import PersonImportForm, PersonUpdateForm

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ('name', 'default_meal_data', 'valid_calories')
    template_name = 'persons/person_create.html'

    def get_success_url(self):
        return reverse('persons:detail',
                       kwargs={'person_name': self.object.name})


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    pk_url_kwarg = 'person_name'
    form_class = PersonUpdateForm
    template_name_suffix = '_update'


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    pk_url_kwarg = 'person_name'

    def get_context_data(self, *args, **kwargs):
        res = super(PersonDetailView, self).get_context_data(*args, **kwargs)
        res['meals'] = self.object.processed_meals()
        return res


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
