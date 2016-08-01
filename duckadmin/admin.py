from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, Http404
from django.core.urlresolvers import reverse
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters


class DuckAdmin(admin.ModelAdmin):
    change_list_template = 'duck_change_list.html'
    duck_form = None

    def get_changelist(self, request, **kwargs):
        self.duck_form._prepare()

        changelist = type(
            'DuckChangeList',
            (ChangeList,),
            {'get_queryset': self.duck_form._default_manager.get_queryset}
        )
        return changelist

    def get_queryset(self, request):
        self.duck_form._prepare()
        return self.duck_form._default_manager.get_queryset(request)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        opts = self.duck_form._meta

        context = {
            'title': self.duck_form._meta.verbose_name_plural,
            'opts': opts,
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
                    self.duck_form.update_data(request, data)
                else:
                    self.duck_form.create_data(request, data)

                self.message_user(request, 'Success', messages.SUCCESS)
                preserved_filters = self.get_preserved_filters(request)

                redirect_url = reverse('admin:%s_%s_changelist' %
                                       (opts.app_label, opts.model_name),
                                       current_app=self.admin_site.name)
                redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts},
                                                     redirect_url)

                return HttpResponseRedirect(redirect_url)

            self.message_user(request, 'Error', messages.ERROR)
        else:
            if object_id:
                try:
                    data = self.duck_form.get_data_by_pk(request, object_id)
                except self.duck_form.DoesNotExist:
                    raise Http404()

                form = self.duck_form(data)
            else:
                form = self.duck_form()

        context['adminform'] = form.as_adminform()
        return render(request, 'admin/change_form.html', context)
