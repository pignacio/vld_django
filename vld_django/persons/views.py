#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import datetime
import json
import logging

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from utils.views import LoginRequiredMixin
from meals.models import Meal
from meals.helper import trim_meals_data
from .helper import make_charts
from .models import Person
from .forms import (PersonImportForm, PersonUpdateForm, PersonCreateValueForm,
                    PersonValuesSelectDatesForm, PersonAddValuesForm)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = (
        'name',
        'owner',
        'timezone',
        'valid_calories',
        'valid_carbs',
        'valid_proteins',
        'valid_fat',
        'valid_fiber',
        'default_meal_data',
    )  # yapf: disable
    template_name = 'persons/person_create.html'

    def get_success_url(self):
        return reverse('persons:detail', kwargs={'person_name': self.object.name})


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


class PersonValuesView(LoginRequiredMixin, DetailView):
    model = Person
    pk_url_kwarg = 'person_name'
    template_name_suffix = '_values'

    def get_context_data(self, *args, **kwargs):
        res = super(PersonValuesView, self).get_context_data(*args, **kwargs)
        start = self.object.meal_set.order_by('date')[0].date
        end = datetime.date.today()
        res['charts'] = [c._replace(options=json.dumps(c.options),
                                    rows=json.dumps(c.rows))
                         for c in make_charts(self.object, start, end)]
        return res


class PersonCreateValueView(LoginRequiredMixin, UpdateView):
    model = Person
    pk_url_kwarg = 'person_name'
    form_class = PersonCreateValueForm
    template_name_suffix = '_create_value'

    def form_valid(self, form):
        self.object.values[form.cleaned_data['name']] = {}
        self.object.save()
        return redirect('persons:values', self.object.name)


class PersonValuesSelectDatesView(LoginRequiredMixin, UpdateView):
    model = Person
    pk_url_kwarg = 'person_name'
    form_class = PersonValuesSelectDatesForm
    template_name_suffix = '_select_dates'

    def form_valid(self, form):
        data = form.cleaned_data
        return redirect('persons:add_values', self.object.name, data['date_start'],
                        data['date_end'])


class PersonAddValuesView(LoginRequiredMixin, UpdateView):
    model = Person
    pk_url_kwarg = 'person_name'
    form_class = PersonAddValuesForm
    template_name_suffix = '_add_values'

    def get_form_kwargs(self, *args, **kwargs):
        res = super(PersonAddValuesView, self).get_form_kwargs(*args, **kwargs)
        res['date_start'] = datetime.datetime.strptime(self.kwargs['date_start'], '%Y-%m-%d')
        res['date_end'] = datetime.datetime.strptime(self.kwargs['date_end'], '%Y-%m-%d')
        return res

    def form_valid(self, form):
        data = form.cleaned_data
        for date, value, field_name in form.get_date_value_field_triplets():
            self.object.values[value][date] = data[field_name]
        self.object.save()
        return redirect('persons:values', self.object.name)
