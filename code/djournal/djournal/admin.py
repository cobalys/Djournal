# -*- coding: utf-8 -*-
'''
Copyright Cobalys.com (c) 2011

This file is part of Djournal.

    Djournal is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Djournal is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Djournal.  If not, see <http://www.gnu.org/licenses/>.
'''
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import widgets, helpers
from django.contrib.admin.options import csrf_protect_m, \
    get_content_type_for_model
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.views.main import TO_FIELD_VAR, IS_POPUP_VAR
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import ModelForm
from django.forms.formsets import all_valid
from django.http.response import Http404
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext as _

from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import unquote
from djournal import djournal_settings
from djournal.fields import TagsField, TagsWidget
from djournal.models import Entry, Tag


def publish(modeladmin, request, queryset):
    queryset.update(published=True)
publish.short_description = _('Publish')


def hide(modeladmin, request, queryset):
    queryset.update(published=False)
hide.short_description = _('Hide')


class EntryAdminForm(ModelForm):
#     tags = ModelMultipleChoiceField(None)

    def __init__(self, *args, **kwargs):
        super(EntryAdminForm, self).__init__(*args, **kwargs)
        choices = self.fields['tags'].widget.choices
        queryset = self.fields['tags'].queryset
        required = self.fields['tags'].required
        self.fields['tags'] = TagsField(queryset, required=required)
        #self.fields['tags'].widget = TagsWidget(choices)  # = ModelMultipleChoiceField(kwargs['instance'].tags)#kwargs['instance'].tags)
        print str(self.fields)

    class Meta:
        model = Entry
        fields = ['tags', ]
        if djournal_settings.RICHTEXT_EDITOR:
            package_name = djournal_settings.RICHTEXT_EDITOR.split('.')
            class_name = package_name[-1]
            del package_name[-1]
            module_name = '.'.join(package_name)
            module = __import__(module_name, fromlist=[class_name])
            widget_class = getattr(module, class_name)
            widgets = {
              'content': widget_class(),
            }


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'slug')
    list_display_links = ('title', 'slug')
    ordering = ('-modification_date',)
    save_on_top = True
    list_per_page = 10
    list_filter = ('published',)
    actions = [publish, hide]
    form = EntryAdminForm

    fieldsets = (
            (None, {
                'fields': ('title', 'slug', 'published', 'content'),
            }),
            (_('Excerpt'), {
                'classes': ('collapse',),
                'fields': ('excerpt',),
            }),
            (_('Tags'), {
                'fields': ('tags',),
            }),
    )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        preserved_filters = self.get_preserved_filters(request)
        form_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, form_url)
        view_on_site_url = self.get_view_on_site_url(obj)
        context.update({
            'add': add,
            'change': change,
            'publish': getattr(obj, 'published', False),
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True,  # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': view_on_site_url is not None,
            'absolute_url': view_on_site_url,
            'form_url': form_url,
            'opts': opts,
            'content_type_id': get_content_type_for_model(self.model).pk,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'to_field_var': TO_FIELD_VAR,
            'is_popup_var': IS_POPUP_VAR,
            'app_label': app_label,
        })
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        else:
            form_template = self.change_form_template

        request.current_app = self.admin_site.name

        return TemplateResponse(request, form_template or [
            "admin/%s/%s/change_form.html" % (app_label, opts.model_name),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ], context)

    @csrf_protect_m
    @transaction.atomic
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta
        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if not self.has_change_permission(request, obj):
                raise PermissionDenied

            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                    'name': force_text(opts.verbose_name), 'key': escape(object_id)})

            if request.method == 'POST' and "_saveasnew" in request.POST:
                return self.add_view(request, form_url=reverse('admin:%s_%s_add' % (
                    opts.app_label, opts.model_name),
                    current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object, change=not add)
            if all_valid(formsets) and form_validated:
                
                if "_publish" in request.POST:
                    new_object.published = True
                elif "_unpublish" in request.POST:
                    new_object.published = False
                
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                if add:
                    self.log_addition(request, new_object)
                    return self.response_add(request, new_object)
                else:
                    change_message = self.construct_change_message(request, form, formsets)
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(request, self.model(), change=False)
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(request, obj, change=True)

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        context = dict(self.admin_site.each_context(request),
            title=(_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
            adminform=adminForm,
            object_id=object_id,
            original=obj,
            is_popup=(IS_POPUP_VAR in request.POST or
                      IS_POPUP_VAR in request.GET),
            to_field=to_field,
            media=media,
            inline_admin_formsets=inline_formsets,
            errors=helpers.AdminErrorList(form, formsets),
            preserved_filters=self.get_preserved_filters(request),
        )

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)


    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        if request.user.is_superuser or request.user.has_perm('djournal.edit_all_entries'):
            qs = self.model._default_manager.get_query_set()
        else:
            qs = self.model._default_manager.get_query_set().filter(user=request.user)
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    class Media:
        css = {
            "all": ("%s%s" % (settings.STATIC_URL, 'djournal/admin/css/djournal-entry.css'),)
        }
        js = (djournal_settings.JQUERY_URL,
              djournal_settings.JQUERYUI_URL,
              "%s%s" % (settings.STATIC_URL, 'admin/js/urlify.js'),
              "%s%s" % (settings.STATIC_URL, 'djournal/admin/js/djournal-entry.js')
              )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    ordering = ('name',)
    save_on_top = True

    class Media:
        js = (djournal_settings.JQUERY_URL,
              djournal_settings.JQUERYUI_URL,
              "%s%s" % (settings.STATIC_URL, 'admin/js/urlify.js'),
              "%s%s" % (settings.STATIC_URL, 'djournal/admin/js/djournal-tag.js')
              )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
