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
import datetime

register = Library()


class TagSidebarNode(template.Node):
    def render(self, context):
        tags_menu_items = cache.get('djournal_tags_menu')
        if not tags_menu_items:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(1), " \
                           "djournal_tag.id, "\
                           "djournal_tag.slug, "\
                           "djournal_tag.name " \
                           "FROM djournal_tag, "\
                           "djournal_entry, "\
                           "djournal_entry_tags "\
                           "WHERE djournal_entry.id = djournal_entry_tags.entry_id "\
                           "AND djournal_tag.id = djournal_entry_tags.tag_id "\
                           "AND djournal_entry.published = 1 "\
                           "GROUP BY djournal_tag.id")
            tags_menu_items = cursor.fetchall()
            cache.set('djournal_tags_menu', tags_menu_items)
        t = get_template('djournal/templatetags/navigation/tag_menu.html')
        c = Context({"tags_menu_items": tags_menu_items, })
        try:
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                # Fail silently for invalid included templates.
                return ''


@register.tag
def djournal_tag_sidebar(parser, token):
    return TagSidebarNode()


class DateSidebarNode(template.Node):
    def render(self, context):
        date_menu_items = cache.get('djournal_date_menu')
        if not date_menu_items:
            cursor = connection.cursor()
            '''
            TODO: This should be tested for each database and abstracted into a
            better separation of logic.
            '''
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
                cursor.execute("SELECT COUNT(*) AS total, " \
                               "MONTH(creation_date) AS month, " \
                               "YEAR(creation_date) AS year " \
                               "FROM djournal_entry v " \
                               "WHERE enabled = 1 " \
                               "GROUP BY YEAR(creation_date), " \
                               "MONTH(creation_date) " \
                               "ORDER BY year DESC, month")
            elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                select = "SELECT COUNT(*) AS total, " \
                         "strftime('%m', creation_date) AS month, " \
                         "strftime('%Y', creation_date) AS year " \
                         "FROM djournal_entry v " \
                         "WHERE published = 1 " \
                         "GROUP BY strftime('%Y', creation_date), " \
                         "strftime('%m', creation_date) " \
                         "ORDER BY year DESC, month"
                cursor.execute(select)
            elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.oracle':
                cursor.execute("SELECT COUNT(*) AS total, " \
                               "to_char(creation_date, 'mm') AS month, " \
                               "to_char(creation_date, 'yyyy') AS year " \
                               "FROM djournal_entry v " \
                               "WHERE published = 1 " \
                               "to_char(creation_date, 'yyyy'), " \
                               "to_char(creation_date, 'mm') " \
                               "ORDER BY year DESC, month")
            elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
                cursor.execute("SELECT COUNT(*) AS total, " \
                               "date_part('month', creation_date) AS month, " \
                               "date_part('year', creation_date) AS year " \
                               "FROM djournal_entry v " \
                               "WHERE published = 1 " \
                               "date_part('year', creation_date) AS year, " \
                               "date_part('month', creation_date) " \
                               "ORDER BY year DESC, month")
            year_dict = {}
            for row in cursor.fetchall():
                total = int(row[0])
                month_number = int(row[1])
                year_number = int(row[2])
                month_name = get_month_name(month_number)
                item = [month_number, month_name, total]
                if year_number in year_dict:
                    year_dict[year_number].append(item)
                else:
                    year_dict[year_number] = []
                    year_dict[year_number].append(item)
            date_menu_items = year_dict.items()
            cache.set('djournal_date_menu', date_menu_items)
        context_dict = {
                        'date_menu_items': date_menu_items,
                        'curfrent_year': datetime.datetime.today().year,
                        'year_expanded': context.get('year_expanded', None)
                        }
        t = get_template('djournal/templatetags/navigation/date_menu.html')
        c = Context(context_dict)
        try:
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                # Fail silently for invalid included templates.
                return ''


@register.tag
def djournal_date_sidebar(parser, token):
    return DateSidebarNode()

