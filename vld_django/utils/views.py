#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class SimpleFormViewMixin(object):
    template_name = 'simple_form.html'
    page_title = 'Page title'

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, *args, **kwargs):
        data = super(SimpleFormViewMixin, self).get_context_data(*args, **kwargs)
        data['page_title'] = self.get_page_title()
        return data
