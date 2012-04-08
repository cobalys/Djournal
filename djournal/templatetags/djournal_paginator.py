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
from django.template import Library, TemplateSyntaxError
from django import template
from django.utils.translation import ugettext as _


class PaginatorSimpleNode(template.Node):
    def __init__(self, pages, page):
        self.pages = template.Variable(pages)
        self.page = template.Variable(page)

    def render(self, context):
        try:
            page = self.page.resolve(context)
            pages = self.pages.resolve(context)
            pages_total = len(pages)
            output = ""
            str_list = []
            if pages_total > 1:
                str_list += "<table class='pagination'>"
                str_list += "<td class='pagination-left'>"
                if page > 1:
                    str_list += "<a class='pagination-left' href='?page=%i'>%s</a>" % (int(page) - 1,_('Previous'))
                str_list += "</td>"
                str_list += "<td class='pagination-center'>"
                str_list += "<span class='pagination-center'>%s %s %s %s</span>" % (_('Page'), str(page),_('of'), str(pages_total))
                str_list += "</td>"
                str_list += "<td class='pagination-right'>"
                if page < pages_total:
                    str_list += "<a class='pagination-right' href='?page=%i'>%s</a>" % (int(page) + 1,_('Next'))
                str_list += "</td>"
                str_list += "</table>"
            return output.join(str_list)
        except template.VariableDoesNotExist:
            return ''

register = Library()
#@register.tag
def djournal_paginator_simple(parser, token):
    bits = token.contents.split()
    if len(bits) < 2:
        raise TemplateSyntaxError(_("Paginator takes two arguments"))
    tagname, pages, page = bits
    return PaginatorSimpleNode(pages, page)

djournal_paginator_simple.is_safe = True
djournal_paginator_simple = register.tag(djournal_paginator_simple)
