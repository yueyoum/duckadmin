from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, Http404

from django.contrib.admin.views.main import ChangeList


class DuckQueryset(object):
    def _clone(self):
        return []

    def __len__(self):
        return 0


class DuckChangeList(ChangeList):
    def get_queryset(self, request):
        return DuckQueryset()


class DuckAdmin(admin.ModelAdmin):
    change_list_template = 'duck_change_list.html'
    duck_form = None

    def get_changelist(self, request, **kwargs):
        return DuckChangeList

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        context = {
            'title': self.duck_form._meta.verbose_name_plural,
            'opts': self.duck_form._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': True,
        }

        if request.method == 'POST':
            form = self.duck_form(request.POST)
            if form.is_valid():

                data = form.cleaned_data
                if object_id:
                    self.duck_form.update_data(data)
                else:
                    self.duck_form.create_data(data)

                messages.success(request, 'Success')
                return HttpResponseRedirect('')

            messages.error(request, 'Error')
        else:
            if object_id:
                try:
                    data = self.duck_form.get_data_by_pk(object_id)
                except self.duck_form.DoesNotExist:
                    raise Http404()

                form = self.duck_form(data)
            else:
                form = self.duck_form()

        context['adminform'] = form.as_adminform()
        return render(request, 'admin/change_form.html', context)
