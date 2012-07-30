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
from django import template
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.template import Library, TemplateSyntaxError, Context
from django.template.loader import get_template
from djournal.helpers.date import get_month_name

register = Library()

class TagNode(template.Node):
    def render(self, context):
        tags_menu_items = cache.get('djournal_tags_menu')
        if not tags_menu_items:
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(1), djournal_tag.id, djournal_tag.slug, djournal_tag.name FROM djournal_tag, djournal_entry, djournal_entry_tags WHERE djournal_entry.id = djournal_entry_tags.entry_id AND djournal_tag.id = djournal_entry_tags.tag_id AND djournal_entry.enabled = 1 GROUP BY djournal_tag.id')
            tags_menu_items = cursor.fetchall()
            cache.set('djournal_tags_menu', tags_menu_items)            
        t = get_template('sidebar/tag_menu.html')
        c = Context({ "tags_menu_items": tags_menu_items,})        
        try:
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return '' # Fail silently for invalid included templates.

#@register.tag
def djournal_tag_nav(parser, token):
    return TagNode()


class DatesNode(template.Node):
    def render(self, context):
        date_menu_items = cache.get('djournal_date_menu')
        if not date_menu_items:
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) AS total, MONTH(modification_date) AS month, YEAR(modification_date) AS year FROM djournal_entry v WHERE enabled = 1 GROUP BY YEAR(modification_date), MONTH(modification_date) ORDER BY year DESC, month')
            year_dict = {}
            for row in cursor.fetchall():
                total = row[0]
                month_number = row[1]
                year_number = row[2]
                month_name = get_month_name(month_number)
                item = [month_number, month_name, total]
                if year_number in year_dict:
                    year_dict[year_number].append(item)
                else:
                    year_dict[year_number] = []
                    year_dict[year_number].append(item)
            date_menu_items = year_dict.items()
            cache.set('djournal_date_menu', date_menu_items)            
        t = get_template('sidebar/date_menu.html')
        c = Context({ "date_menu_items": date_menu_items,})        
        try:
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return '' # Fail silently for invalid included templates.
 
#@register.tag
def djournal_dates_nav(parser, token):
    return DatesNode()


djournal_tag_nav.is_safe = True
djournal_dates_nav.is_safe = True
djournal_tag_nav = register.tag(djournal_tag_nav)
djournal_dates_nav = register.tag(djournal_dates_nav)