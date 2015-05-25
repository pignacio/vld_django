#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging
import json

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import floppyforms.__future__ as forms
from var_log_dieta.objects import NutritionalValue, Ingredient as VldIngredient

from .models import Ingredient

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

_FLOAT_FIELDS = ('calories', 'carbs', 'protein', 'sugar', 'fat', 'trans_fat',
                 'saturated_fat', 'fiber', 'sample_size')


class IngredientForm(forms.ModelForm):
    class Meta(object):
        model = Ingredient
        fields = ('name', )

    sample_size = forms.FloatField(label=_('Cantidad'),
                                   min_value=0,
                                   initial=100)
    sample_unit = forms.CharField(label=_('Unidad'), initial='g')

    calories = forms.FloatField(label=_('Calorías'),
                                min_value=0,
                                required=False)
    carbs = forms.FloatField(label=_('Carbs'), min_value=0, required=False)
    sugar = forms.FloatField(label=_('Azúcar'), min_value=0, required=False)
    protein = forms.FloatField(label=_('Proteínas'),
                               min_value=0,
                               required=False)
    fat = forms.FloatField(label=_('Grasas'), min_value=0, required=False)
    trans_fat = forms.FloatField(label=_('Grasas Trans'),
                                 min_value=0,
                                 required=False)
    saturated_fat = forms.FloatField(label=_('Grasas Saturadas'),
                                     min_value=0,
                                     required=False)
    fiber = forms.FloatField(label=_('Fibra'), min_value=0, required=False)

    conversions = forms.CharField(label=_('Conversiones'), required=False)
    categories = forms.CharField(label=_('Categorías'), required=False)

    def __init__(self, *args, **kwargs):
        res = super(IngredientForm, self).__init__(*args, **kwargs)
        for field_name in _FLOAT_FIELDS:
            self.fields[field_name].widget.attrs['step'] = 0.01
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'sample_size',
            'sample_unit',
            'calories',
            'carbs',
            'sugar',
            'fat',
            'trans_fat',
            'saturated_fat',
            'fiber',
            'conversions',
            'categories',
            FormActions(Submit('submit', _('Agregar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Agregando...')), )
        )  # yapf: disable

    def clean_name(self):
        if Ingredient.objects.filter(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError(
                _('Ya hay un ingrediente con ese nombre.'))
        return self.cleaned_data['name']

    def clean_conversions(self):
        try:
            conversions = self.cleaned_data['conversions']
            if conversions == '':
                return {}
            return json.loads(conversions)
        except ValueError:

            raise forms.ValidationError(_('No es un object JSON válido.'))

    def clean_categories(self):
        return [c.strip() for c in self.cleaned_data['categories'].split(',')
                if c.strip()]

    def save(self):
        logger.debug("data: %s", self.cleaned_data)
        self.cleaned_data['sample_value'] = NutritionalValue(*[
            self.cleaned_data[f] for f in NutritionalValue._fields
        ])
        ingredient = VldIngredient(*[self.cleaned_data[f]
                                     for f in VldIngredient._fields])
        logger.debug('ingredient: %s', ingredient)
        self.instance.save_as(ingredient)
        return self.instance


class IngredientImportForm(forms.ModelForm):
    class Meta(object):
        model = Ingredient
        fields = ('data', )

    def __init__(self, *args, **kwargs):
        super(IngredientImportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'data',
            FormActions(Submit('submit', _('Importar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Importando...')), )
        )  # yapf: disable

    def clean_data(self):
        try:
            ingredient = VldIngredient.from_json(self.cleaned_data['data'])
        except Exception as err:
            raise forms.ValidationError(_('No es un ingrediente válido'))
        else:
            if Ingredient.objects.filter(name=ingredient.name).exists():
                raise forms.ValidationError(
                    _('Ya hay un ingrediente con ese nombre.'))
            self.cleaned_data['ingredient'] = ingredient
            return self.cleaned_data['data']

    def save(self, *args, **kwargs):
        self.instance.save_as(self.cleaned_data['ingredient'])
        return self.instance


class IngredientMassImportForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea(), label=_('Data'))

    def __init__(self, *args, **kwargs):
        super(IngredientMassImportForm, self).__init__(*args, **kwargs)
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
            raise forms.ValidationError('No es un object JSON válido.')
        if not isinstance(data, list):
            data = [data]
        return data

