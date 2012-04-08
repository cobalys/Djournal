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
from django.db import connection
from django.template import Context
from django.template.loader import get_template
from djournal.helpers.date import get_month_name
import codecs


def generate_date_menu():
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) AS total, MONTH(modification_date) AS month, YEAR(modification_date) AS year FROM djournal_entry v WHERE enabled = 1 GROUP BY YEAR(modification_date), MONTH(modification_date) ORDER BY year DESC, month')
    year_dict = {}
    for row in cursor.fetchall():
        total = row[0]
        month_number = row[1]
        year_number = row[2]
        month_name = get_month_name(month_number)
        set = [month_number, month_name, total]
        if year_number in year_dict:
            year_dict[year_number].append(set)
        else:
            year_dict[year_number] = []
            year_dict[year_number].append(set)
    t = get_template('generate/date_menu.html')
    c = Context({ "year_dict": year_dict.items(),})
    output = t.render(c)
    gendir = '%sdjournal/date_menu.html' % settings.GENERATOR_DIR
    f = codecs.open(gendir, "w")
    try:
        f.write(output)
    finally:
        f.close()


def generate_tag_files():
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(1), djournal_tag.id, djournal_tag.slug, djournal_tag.name FROM djournal_tag, djournal_entry, djournal_entry_tags WHERE djournal_entry.id = djournal_entry_tags.entry_id AND djournal_tag.id = djournal_entry_tags.tag_id AND djournal_entry.enabled = 1 GROUP BY djournal_tag.id')
    tags = cursor.fetchall()
    t = get_template('generate/tag_menu.html')
    c = Context({ "tags": tags,})
    output = t.render(c)
    try:
        gendir = '%s/djournal/tag_menu.html' % settings.GENERATOR_DIR
        f = codecs.open(gendir, "w")
        try:
            f.write(output)
        finally:
            f.close()
    except IOError:
        pass
