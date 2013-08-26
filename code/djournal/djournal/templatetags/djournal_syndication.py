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
from django.template import Library, TemplateSyntaxError
from django.template.context import Context
from django.template.loader import get_template
from djournal import djournal_settings


register = Library()


class RssHeadNode(template.Node):

    def render(self, context):
        tag = context.get('tag', None)
        t = get_template('djournal/templatetags/syndication/rss_head_links.html')
        try:
            c = Context({
                         'tag': tag,
                         'title': djournal_settings.TITLE,
                        })
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return ''# Fail silently for invalid included templates.


@register.tag
def djournal_rss_head(parser, token):
    return RssHeadNode()


class RssBodyAllNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        inner_code = self.nodelist.render(context)
        t = get_template('djournal/templatetags/syndication/rss_body_all.html')
        try:
            c = Context({
                         'inner_code': inner_code,
                         'title': djournal_settings.TITLE,
                        })
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return ''#Fail silently for invalid included templates.


@register.tag
def djournal_rss_body_all(parser, token):
    nodelist = parser.parse(('end_djournal_rss_body_all',))
    parser.delete_first_token()
    return RssBodyAllNode(nodelist)


class RssBodyTagNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        inner_code = self.nodelist.render(context)
        tag = context.get('tag')
        if tag == None:
            return ''
        try:
            c = Context({
                         'tag': tag,
                         'inner_code': inner_code,
                         'title': djournal_settings.TITLE,
                        })
            t = get_template('djournal/templatetags/syndication/rss_body_all.html')
            return t.render(c)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included template had syntax error: %s]" % e
            else:
                return ''# Fail silently for invalid included templates.


@register.tag
def djournal_rss_body_tag(parser, token):
    nodelist = parser.parse(('end_djournal_rss_body_tag',))
    parser.delete_first_token()
    return RssBodyTagNode(nodelist)
