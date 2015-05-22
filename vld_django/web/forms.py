#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.utils.translation import ugettext as _
from django.contrib import auth
import floppyforms.__future__ as forms

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
            'class': 'form-control'}))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'class': 'form-control'}))
    next = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data['username']
        password = cleaned_data['password']

        user = cleaned_data['user'] = auth.authenticate(username=username,
                                                        password=password)

        if not user:
            raise forms.ValidationError(_('Username or password invalid.'))

        return cleaned_data
