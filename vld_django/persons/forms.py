#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import datetime
import json
import logging

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
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
            return {datetime.datetime.strptime(k, '%Y-%m-%d').date(): v for k, v in items}
        except ValueError:
            raise forms.ValidationError('Una de las fechas no fue valida.')

        return data


class PersonUpdateForm(forms.ModelForm):
    class Meta(object):
        model = Person
        fields = (
            'default_meal_data',
            'valid_calories',
            'valid_carbs',
            'valid_proteins',
            'valid_fat',
            'valid_fiber',
            'charts',
            'timezone',
            'owner',
        )  # yapf: disable

    def __init__(self, *args, **kwargs):
        super(PersonUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'owner',
            'timezone',
            'valid_calories',
            'valid_carbs',
            'valid_proteins',
            'valid_fat',
            'valid_fiber',
            'charts',
            'default_meal_data',
            FormActions(
                Submit('submit', _('Guardar'),
                       css_class='btn-primary pull-right',
                       data_loading_text=_('Guardando...')), )
        )  # yapf: disable


class PersonCreateValueForm(forms.Form):
    name = forms.CharField()

    def __init__(self, instance, *args, **kwargs):
        super(PersonCreateValueForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            FormActions(Submit('submit', _('Agregar'),
                               css_class='btn-primary pull-right',
                               data_loading_text=_('Agregando...')), )
        )  # yapf: disable

    def clean_name(self):
        name = self.cleaned_data['name']
        if name in self.instance.values:
            raise forms.ValidationError(_('Ya hay un valor con ese nombre.'))
        return name


class PersonValuesSelectDatesForm(forms.Form):
    date_start = forms.DateField(label=_('Inicio'))
    date_end = forms.DateField(label=_('Final'))

    def __init__(self, instance, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        initial.update({
            'date_start': instance.today_date().strftime("%F"),
            'date_end': instance.today_date().strftime("%F"),
        })
        kwargs['initial'] = initial
        super(PersonValuesSelectDatesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            'date_start',
            'date_end',
            Submit('submit', _('Siguiente'),
                   css_class='btn-primary', ) ,
        )  # yapf: disable


class PersonAddValuesForm(forms.Form):
    def __init__(self, instance, date_start, date_end, *args, **kwargs):
        if date_start > date_end:
            raise ValueError('date_start is greater than date_end')
        self.instance = instance
        self.date_start = date_start
        self.date_end = date_end
        fields_by_date = self._generate_fields()
        super(PersonAddValuesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(HTML('<table class="table"><thead><tr><th>Valor</th>'))

        date = self.date_start
        fields = []
        while date <= self.date_end:
            self.helper.layout.append(HTML('<th>{}</th>'.format(date.strftime('%F'))))
            date += datetime.timedelta(days=1)

        self.helper.layout.append(HTML("</tr></thead><tbody>"))

        for value, fields in fields_by_date:
            self.helper.layout.append(HTML("<tr><td>{}</td>".format(value)))
            for field in fields:
                self.fields[field['field_name']] = forms.FloatField(initial=field['initial'],
                                                                    required=False)
                self.fields[field['field_name']].widget.attrs['step'] = 'any'
                self.helper.layout.append(HTML("<td>"))
                self.helper.layout.append(field['field_name'])
                self.helper.layout.append(HTML("</td>"))
            self.helper.layout.append(HTML("</tr>"))
        self.helper.layout.append(HTML("</tbody></table>"))
        self.helper.layout.append(FormActions(Submit('submit', _('Guardar'),
                                                     css_class='btn-primary pull-right',
                                                     data_loading_text=_('Guardando...')), ))

    def _generate_fields(self):
        values_by_fields = []
        for value, values in sorted(self.instance.values.items()):
            date = self.date_start
            fields = []
            while date <= self.date_end:
                date_str = date.strftime('%F')
                fields.append({
                    'initial': values.get(date_str, None),
                    'field_name': "{}_{}".format(value, date_str),
                    'value': value,
                    'date': date_str
                })
                date += datetime.timedelta(days=1)
            values_by_fields.append((value, fields))

        return values_by_fields

    @staticmethod
    def _get_initial(fields_by_date):
        initial = {}
        for fields in fields_by_date.values():
            for field in fields:
                initial[field['field_name']] = field['initial']

    def get_date_value_field_triplets(self):
        for _value, fields in self._generate_fields():
            for field in fields:
                yield field['date'], field['value'], field['field_name']
