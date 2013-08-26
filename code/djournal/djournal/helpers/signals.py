# -*- coding: utf-8 -*-
'''
Copyright Cobalys.com (c) 2011

This file is part of Djournal.

    Djournal is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Djournal is distributed in the hope that it will be useful,
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Djournal.  If not, see <http://www.gnu.org/licenses/>.
'''
from django.core.cache import cache


def clean_cache_signal(sender, **kwargs):
    cache.delete('djournal_tags_menu')
    cache.delete('djournal_date_menu')
    cache.delete('djournal-syndication-entries-latest')
    cache.delete('djournal_entries_by_tag_syndication')
    cache.delete('djournal_entries_sitemap')
