#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import datetime
import json
import logging

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import floppyforms.__future__ as forms

from .models import Person

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PersonImportForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea())

    def __init__(self, instance, *args, **kwargs):
        super(PersonImportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'data',
            FormActions(Submit('submit', _('Importar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Importando...')), )
        )  # yapf: disable

    def clean_data(self):
        try:
            data = json.loads(self.cleaned_data['data'])
        except ValueError:
            raise forms.ValidationError('No es un objeto JSON válido.')
        try:
            items = data.items()
        except AttributeError:
            raise forms.ValidationError('No es un diccionario JSON válido.')

        try:
            return {
                datetime.datetime.strptime(k, '%Y-%m-%d').date(): v
                for k, v in items
            }
        except ValueError:
            raise forms.ValidationError('Una de las fechas no fue valida.')

        return data


class PersonUpdateForm(forms.ModelForm):
    class Meta(object):
        model = Person
        fields = ('default_meal_data', 'valid_calories', )

    def __init__(self, *args, **kwargs):
        super(PersonUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'default_meal_data',
            'valid_calories',
            FormActions(
                Submit('submit', _('Guardar'),
                       css_class='btn-primary pull-right',
                       data_loading_text=_('Guardando...')), )
        )  # yapf: disable
