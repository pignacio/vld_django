#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-many-ancestors
from __future__ import absolute_import, unicode_literals, division

import datetime
import json
import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView

from ingredient.helper import get_ingredients_data
from utils.views import LoginRequiredMixin
from persons.models import Person
from .forms import MealCreateForm, MealAddSectionForm, MealEditSectionForm, MealPhotoCreateForm
from .helper import process_meal_data
from .models import Meal, MealPhoto

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def get_default_meal(person_name, date):
    person = get_object_or_404(Person, name=person_name)
    if isinstance(date, basestring):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    try:
        return Meal.objects.get(person=person, date=date)
    except Meal.DoesNotExist:
        return Meal(person=person,
                    date=date,
                    data=person.default_meal_data)

class MealViewMixin(LoginRequiredMixin):
    def get_object(self):
        return get_default_meal(self.kwargs['person_name'], self.kwargs['date'])

    def get_context_data(self, *args, **kwargs):
        res = super(MealViewMixin, self).get_context_data(*args, **kwargs)
        if self.object:
            res['next_meal_date'] = self.object.date + datetime.timedelta(1)
            res['prev_meal_date'] = self.object.date - datetime.timedelta(1)
        return res


class MealCreateView(MealViewMixin, CreateView):
    model = Meal
    template_name_suffix = '_create'
    form_class = MealCreateForm

    def get_form_kwargs(self, *args, **kwargs):
        res = super(MealCreateView, self).get_form_kwargs(*args, **kwargs)
        res['person'] = get_object_or_404(Person,
                                          name=self.kwargs['person_name'])
        return res


class MealDetailView(MealViewMixin, DetailView):
    model = Meal


class MealAddSectionView(MealViewMixin, UpdateView):
    model = Meal
    form_class = MealAddSectionForm
    template_name_suffix = '_add_section'

    def get_context_data(self, *args, **kwargs):
        data = super(MealAddSectionView, self).get_context_data(*args,
                                                                **kwargs)
        data['path'] = self.kwargs['path']
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
        data['ingredients'] = json.dumps(get_ingredients_data(), indent=1)
        data['path'] = self.kwargs['path']
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


def meal_toggle_free(_request, person_name, date):
    person = get_object_or_404(Person, name=person_name)
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    meal, _created = Meal.objects.get_or_create(person=person, date=date)
    meal.is_free = not meal.is_free
    meal.save()
    return redirect(meal.get_absolute_url())


@csrf_exempt
def meal_counter(request, person_name, date, path):
    log = None
    day_log = None
    form = MealEditSectionForm(data=request.POST,
                               instance=None,
                               ingredients=None)
    if form.is_valid():
        ingredients = form.cleaned_data['ingredients']
        meal = get_default_meal(person_name, date)
        data = meal.data
        path = [p for p in path.split('.') if p]
        for key in path:
            data = data.get(key, {})
        data['__init__'] = ingredients

        log = process_meal_data(
            'TOTAL', {'__init__': form.cleaned_data['ingredients']})

        day_log = process_meal_data('DAY TOTAL', meal.data)._replace(parts=[log])

        return render(request, 'meals/meal_log.html', {'log': day_log})


class MealCreatePhotoView(LoginRequiredMixin, CreateView):
    model = MealPhoto
    form_class = MealPhotoCreateForm
    template_name_suffix = '_create'

    def get_form_kwargs(self, *args, **kwargs):
        res = super(MealCreatePhotoView, self).get_form_kwargs(*args, **kwargs)
        person = get_object_or_404(Person, name=self.kwargs['person_name'])
        date = datetime.datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        meal, _created = Meal.objects.get_or_create(person=person,
                                                    date=date,
                                                    defaults={'data': person.default_meal_data})
        res['instance'] = self.model(meal=meal, path=self.kwargs['path'])

        return res

    def get_success_url(self):
        return self.object.meal.get_absolute_url()
