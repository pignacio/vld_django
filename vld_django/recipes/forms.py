#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Button
import floppyforms.__future__ as forms

from .models import Recipe

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class RecipeForm(forms.ModelForm):
    class Meta(object):
        model = Recipe
        fields = (
            'name',
            'amount',
            'unit',
        )  # yapf: disable

    ingredients = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        initial = kwargs.pop('initial', {})
        initial['ingredients'] = '\n'.join(instance.ingredients if instance else [])
        super(RecipeForm, self).__init__(*args, initial=initial, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'amount',
            'unit',
            'ingredients',
            HTML('''
            <div class="row">
               <div class="col-md-8" id="meal-counter"></div>
               <div class="col-md-4" id="ingredient-finder">
                 <div class="panel ingredient-finder-panel" id='ingredient-finder-results'></div>
               </div>
            </div>'''),
            FormActions(Submit('submit', _('Agregar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Agregando...')),
                        Button('meal-counter-button', _('Calcular'),
                               css_id='meal-counter-button',
                               css_class='pull-right'), )
        )  # yapf: disable

    def save(self, *args, **kwargs):
        self.instance.ingredients = self.cleaned_data['ingredients']
        return super(RecipeForm, self).save(*args, **kwargs)

    def clean_ingredients(self):
        data = self.cleaned_data['ingredients']
        if data:
            return [l.strip() for l in data.split('\n')]
        return data
