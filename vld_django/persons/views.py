#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import (ListView, DetailView, RedirectView,
                                  CreateView)

from utils.views import LoginRequiredMixin
from .models import Person

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


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
