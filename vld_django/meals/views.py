#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import datetime
import logging

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (ListView, DetailView, RedirectView,
                                  CreateView, UpdateView)

from utils.views import LoginRequiredMixin
from persons.models import Person
from .forms import MealCreateForm, MealAddSectionForm, MealEditSectionForm
from .helper import process_meal_data
from .models import Meal

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MealViewMixin(LoginRequiredMixin):
    def get_object(self):
        person = get_object_or_404(Person, name=self.kwargs['person_name'])
        date = datetime.datetime.strptime(self.kwargs['date'],
                                          '%Y-%m-%d').date()
        try:
            return Meal.objects.get(person=person, date=date)
        except Meal.DoesNotExist:
            return Meal(person=person, date=date, data={})

    def get_context_data(self, *args, **kwargs):
        res = super(MealViewMixin, self).get_context_data(*args, **kwargs)
        res['next_meal_date'] = self.object.date + datetime.timedelta(1)
        res['prev_meal_date'] = self.object.date - datetime.timedelta(1)
        return res


class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    template_name_suffix = '_create'
    form_class = MealCreateForm

    def get_form_kwargs(self, *args, **kwargs):
        res = super(MealCreateView, self).get_form_kwargs(*args, **kwargs)
        res['person'] = get_object_or_404(Person,
                                          name=self.kwargs['person_name'])
        return res

    def get_success_url(self):
        return self.object.get_success_url()


class MealDetailView(MealViewMixin, DetailView):
    model = Meal

    def get_context_data(self, *args, **kwargs):
        data = super(MealDetailView, self).get_context_data(*args, **kwargs)
        data['log'] = process_meal_data(self.object)
        return data


class MealAddSectionView(MealViewMixin, UpdateView):
    model = Meal
    form_class = MealAddSectionForm
    template_name_suffix = '_add_section'

    def get_context_data(self, *args, **kwargs):
        data = super(MealAddSectionView, self).get_context_data(*args,
                                                                **kwargs)
        data['path'] = self.kwargs['path']
        data['name'] = data['meal'].person.name
        #TODO(pignacio): Fix this strange lookup. meal.person.name does not
        # show on the template
        logger.debug('DATA: %s', data)
        return data


    def form_valid(self, form):
        path = [p for p in self.kwargs['path'].split('.') if p]
        data = self.object.data
        for name in path:
            try:
                data = data[name]
            except KeyError:
                data[name] = {}
                data = data[name]
        data[form.cleaned_data['name']] = {}
        self.object.save()
        return redirect(self.object.get_absolute_url())


class MealEditSectionView(MealViewMixin, UpdateView):
    model = Meal
    form_class = MealEditSectionForm
    template_name_suffix = '_edit_section'

    def get_context_data(self, *args, **kwargs):
        data = super(MealEditSectionView, self).get_context_data(*args,
                                                                 **kwargs)
        data['path'] = self.kwargs['path']
        data['name'] = data['meal'].person.name
        # TODO(pignacio): Fix this strange lookup. meal.person.name does not
        #     show on the template
        logger.debug('DATA: %s', data)
        return data

    def get_form_kwargs(self, *args, **kwargs):
        res = super(MealEditSectionView, self).get_form_kwargs(*args, **kwargs)
        path = [p for p in self.kwargs['path'].split('.') if p]
        data = self.object.data
        for name in path:
            try:
                data = data[name]
            except KeyError:
                data[name] = {}
                data = data[name]
        res['ingredients'] = data.get('__init__', [])
        return res

    def form_valid(self, form):
        path = [p for p in self.kwargs['path'].split('.') if p]
        data = self.object.data
        for name in path:
            try:
                data = data[name]
            except KeyError:
                data[name] = {}
                data = data[name]
        data['__init__'] = form.cleaned_data['ingredients']
        self.object.save()
        return redirect(self.object.get_absolute_url())
