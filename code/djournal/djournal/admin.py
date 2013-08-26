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
from django import forms, template
from django.conf import settings, settings
from django.conf.urls import patterns
from django.contrib import admin, messages
from django.contrib.admin import widgets, helpers
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.util import unquote, flatten_fieldsets, \
    get_deleted_objects, model_format_dict
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError, \
    ValidationError, PermissionDenied
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import models, transaction, router, transaction
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields import BLANK_CHOICE_DASH, FieldDoesNotExist
from django.db.models.related import RelatedObject
from django.db.models.sql.constants import QUERY_TERMS
from django.forms import ModelForm
from django.forms.formsets import all_valid, all_valid
from django.forms.models import modelform_factory, modelformset_factory, \
    inlineformset_factory, BaseInlineFormSet, ModelChoiceField
from django.forms.util import flatatt
from django.forms.widgets import Widget, SelectMultiple, MultipleHiddenInput
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils import six
from django.utils.datastructures import SortedDict
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import escape, escapejs
from django.utils.safestring import mark_safe, mark_safe
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _, ugettext as _, ungettext
from django.views.decorators.csrf import csrf_protect
from djournal import djournal_settings
from djournal.fields import TagsField, TagsWidget
from djournal.models import Entry, Tag
from functools import update_wrapper, partial
import copy
import warnings


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
        self.fields['tags'].widget = TagsWidget(choices) #= ModelMultipleChoiceField(kwargs['instance'].tags)#kwargs['instance'].tags)
        print str(self.fields)

    class Meta:
        model = Entry
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
    list_filter = ('published', )
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
        ordered_objects = opts.get_ordered_objects()
        context.update({
            'add': add,
            'change': change,
            'publish': getattr(obj, 'published', False),
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'ordered_objects': ordered_objects,
            'form_url': form_url,
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
        })
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        else:
            form_template = self.change_form_template

        return TemplateResponse(request, form_template or [
            "admin/%s/%s/change_form.html" % (app_label, opts.object_name.lower()),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ], context, current_app=self.admin_site.name)


    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        inline_instances = self.get_inline_instances(request, None)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                new_object = self.save_form(request, form, change=False)
                form_validated = True
            else:
                form_validated = False
                new_object = self.model()
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new="_saveasnew" in request.POST,
                                  prefix=prefix, queryset=inline.queryset(request))
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                if "_publish" in request.POST:
                    new_object.published = True
                elif "_unpublish" in request.POST:
                    new_object.published = False
                self.save_model(request, new_object, form, False)
                self.save_related(request, form, formsets, False)
                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.get_prepopulated_fields(request),
            self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            prepopulated = dict(inline.get_prepopulated_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, prepopulated, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_text(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'media': media,
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)
    
    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, form_url='', extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url=reverse('admin:%s_%s_add' %
                                    (opts.app_label, opts.module_name),
                                    current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)
        formsets = []
        inline_instances = self.get_inline_instances(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, new_object), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object, prefix=prefix,
                                  queryset=inline.queryset(request))

                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                if "_publish" in request.POST:
                    new_object.published = True
                elif "_unpublish" in request.POST:
                    new_object.published = False
                self.save_model(request, new_object, form, True)
                self.save_related(request, form, formsets, True)
                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, prepopulated, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_text(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': "_popup" in request.REQUEST,
            'media': media,
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj, form_url=form_url)


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
              "%s%s" % (settings.STATIC_URL, 'djournal/admin/js/djournal-tags.js')
              )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
