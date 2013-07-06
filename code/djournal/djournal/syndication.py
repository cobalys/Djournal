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
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from djournal import djournal_settings
from djournal.models import Entry, Tag


class RssEntries(Feed):
    title = djournal_settings.TITLE
    link = reverse_lazy('djournal-syndication-entries')
    description = djournal_settings.SYNDICATION_DESCRIPTION

    def items(self):
        entries_syndication = cache.get('djournal_entries_syndication')
        if not entries_syndication:
            entries_syndication = Entry.objects.filter(published=True)
            cache.set('djournal_entries_syndication', entries_syndication)
        return entries_syndication

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content


class RssEntriesByTag(Feed):
    title = djournal_settings.TITLE
    link = lambda self, obj: reverse_lazy('djournal-syndication-entries-tag', args=[obj.id])
    description = djournal_settings.SYNDICATION_DESCRIPTION

    def get_object(self, request, tag_id):
        return get_object_or_404(Tag, pk=tag_id)

    def items(self, obj):
        entries_syndication = cache.get('djournal_entries_by_tag_syndication')
        if not entries_syndication:
            entries_syndication = obj.entry_set.filter(published=True)
            cache.set('djournal_entries_by_tag_syndication', entries_syndication)
        return entries_syndication

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

