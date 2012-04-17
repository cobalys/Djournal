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
from django.contrib import admin
from django.utils.translation import ugettext as _
from djournal import djournal_settings
from djournal.models import Entry, Tag

def enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
enable.short_description = _('Enable')

def disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
disable.short_description = _('Disable')
    
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'slug')
    list_display_links = ('title', 'slug')
    ordering = ('title',)
    save_on_top = True
    list_per_page = 10
    readonly_fields = ('tags',) 
    fieldsets = (
            (None, {
                'fields': ('title', 'slug', 'enabled', 'content'),
            }),
            (_('Description'), {
                'classes': ('collapse',),
                'fields': ('description',),
            }),
            (_('Tags'), {
                'fields': ('tags',),
            }),
    )

    def save_tags(self, tags_string, entry):
        if tags_string.strip():
            tags = tags_string.lower().split(',')
            print "This is what i got " + str(entry)
            if entry:
                entry.tags.clear()
            for tag_name in tags:
                tag_name = tag_name.strip()
                if len(tag_name):
                    if Tag.objects.filter(name__iexact=tag_name).count():
                        tag = Tag.objects.get(name__iexact=tag_name)
                    else:
                        tag = Tag()
                        tag.name = tag_name
                        tag.save()
                    entry.tags.add(tag)
        entry.save()
        
    class Media:
        js = (djournal_settings.JQUERY_URL, djournal_settings.JQUERYUI_URL)


    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()
        tags = request.POST['tags']
        self.save_tags(tags, obj)

    
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    ordering = ('name',)
    save_on_top = True    
    class Media:
        js = (djournal_settings.JQUERY_URL, djournal_settings.JQUERYUI_URL)



admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
