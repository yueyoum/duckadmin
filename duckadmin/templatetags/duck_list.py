# -*- coding: utf-8 -*-
"""
Author:         Wang Chao <yueyoum@gmail.com>
Filename:       duck_result_list
Date Created:   2015-12-12 19:37
Description:

"""


from django import template
from django.utils.html import format_html, mark_safe

register = template.Library()

class Header(object):
    def __init__(self, name):
        self.sortable = False
        self.text = name
        self.class_attrib = format_html(' class="column-{}"', name)
#
# class Checkbox(Header):
#     def __init__(self):
#         super(Checkbox, self).__init__('')
#         self.class_attrib = mark_safe(' class="action-checkbox-column"')

class Row(object):
    class form:
        non_field_errors = False

    def __init__(self, fields):
        self.fields = fields
        self.text = []

    def add(self, data, app_label, model_name):
        for index, key in enumerate(self.fields):
            value = data[key]

            if index == 0:
                text = u'<th class="field-{0}"><a href="/admin/{1}/{2}/{3}/">{3}</a></th>'.format(
                    key, app_label, model_name, value
                )
            else:
                text = u'<td class="field-{0}">{1}</td>'.format(key, value)

            self.text.append(format_html(text))

    def __iter__(self):
        for i in self.text:
            yield i


class Results(object):
    def __init__(self, model_class):
        self.fields = model_class.declared_fields
        self.app_label = model_class.app_label
        self.model_name = model_class.model_name
        self.rows = []

    def add_row(self, data):
        row = Row(self.fields)
        row.add(data, self.app_label, self.model_name)
        self.rows.append(row)

    def headers(self):
        for i in self.fields:
            yield Header(i)

    def results(self):
        for i in self.rows:
            yield i


@register.inclusion_tag('admin/change_list_results.html')
def duck_result_list(cl):
    results = Results(cl.model)

    for data in cl.model.get_data():
        results.add_row(data)

    return {
        'cl': cl,
        'result_hidden_fields': [],
        'result_headers': results.headers(),
        'num_sorted_fields': 0,
        'results': results.results()
    }
