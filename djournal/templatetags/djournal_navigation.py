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
from django.template import Library, TemplateSyntaxError, Template, Context
from djournal import djournal_settings

register = Library()

class TagNode(template.Node):
    def render(self, context):
        filepath = '%sdjournal/tag_menu.html' % djournal_settings.GENERATOR_DIR
        try:
            fp = open(filepath, 'r')
            output = fp.read()
            fp.close()
        except IOError:
            output = ""
        try:
            t = Template(output, name=filepath)
            c = Context()
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return '' # Fail silently for invalid included templates.
        return output

#@register.tag
def djournal_tag_nav(parser, token):
    return TagNode()


class DatesNode(template.Node):
    def render(self, context):
        filepath = '%sdjournal/date_menu.html' % djournal_settings.GENERATOR_DIR
        try:
            fp = open(filepath, 'r')
            output = fp.read()
            fp.close()
            t = Template(output, name=filepath)
            return t.render(context)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return '' # Fail silently for invalid included templates.
        return output

#@register.tag
def djournal_dates_nav(parser, token):
    return DatesNode()


djournal_tag_nav.is_safe = True
djournal_dates_nav.is_safe = True
djournal_tag_nav = register.tag(djournal_tag_nav)
djournal_dates_nav = register.tag(djournal_dates_nav)