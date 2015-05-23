#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button
import floppyforms.__future__ as forms

from .models import Meal

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MealCreateForm(forms.ModelForm):
    class Meta(object):
        model = Meal
        fields = ('date', )

        widgets = {'date': forms.DateInput(), }

    def __init__(self, person, *args, **kwargs):
        super(MealCreateForm, self).__init__(*args, **kwargs)
        self.instance.person = person
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'date',
            FormActions(Submit('submit', _('Agregar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Agregando...')), )
        )  # yapf: disable

    def clean_date(self):
        date = self.cleaned_data['date']
        if (self.instance.person.meal_set.filter(date=date).exists()):
            raise forms.ValidationError('Ya hay una comida para esa fecha.')
        return date


class MealAddSectionForm(forms.Form):
    name = forms.CharField()

    def __init__(self, instance, *args, **kwargs):
        super(MealAddSectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            FormActions(Submit('submit', _('Agregar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Agregando...')), )
        )  # yapf: disable


class MealEditSectionForm(forms.Form):
    ingredients = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, instance, ingredients, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        initial['ingredients'] = '\n'.join(i.strip()
                                           for i in ingredients or [])
        super(MealEditSectionForm, self).__init__(*args,
                                                  initial=initial, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'ingredients',
            FormActions(Submit('submit', _('Agregar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Agregando...')),
                        Button('meal-counter-button', _('Calcular'),
                               css_id='meal-counter-button',
                               css_class='pull-right'),
                        )
        )  # yapf: disable

    def clean_ingredients(self):
        data = self.cleaned_data['ingredients']
        if data:
            return [l.strip() for l in data.split('\n')]
        return data
