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
from django.conf.urls.defaults import patterns, url
from djournal.views import entry, entries_year, entries_month, entries_day, \
    entries_tag, entries_all, get_tag_names


urlpatterns = patterns(
    '',   
    url(r'^permalink/(?P<post_id>\d+)$', entry, name='djournal-entry-permalink'),
    url(r'^(?P<year>\d{4})/entries.html$', entries_year, name='djournal-entries-year'),
    url(r'^(?P<month>\d+)/(?P<year>\d{4})/entries.html$', entries_month, name='djournal-entries-month'),
    url(r'^(?P<day>\d{2})/(?P<month>\d+)/(?P<year>\d{4})/entries.html$', entries_day, name='djournal-entries-day'),
    url(r'^tag/(?P<tag_id>\d+)/([\w-]+)/entries.html$', entries_tag, name='djournal-entries-tag'),
    url(r'^entries.html$', entries_all, name='djournal-entries-all'),
    url(r'^tags.json$', get_tag_names, name='djournal-entries-tags-json'),
    url(r'^(?P<entry_id>\d+)/([\w-]+).html$', entry, name='djournal-entry'),
    url(r'^$', entries_all, name='djournal-entries-index'),

)
