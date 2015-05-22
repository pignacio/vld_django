#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import TemplateView

from utils.views import LoginRequiredMixin
from .forms import LoginForm

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def login(request):
    logger.debug("LOGIN")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return redirect(form.cleaned_data['next'])
    else:
        initial = {'next': request.GET.get('next', 'home')}
        form = LoginForm(initial=initial)

    return render(request, 'web/login.html', {'form': form})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'web/home.html'
