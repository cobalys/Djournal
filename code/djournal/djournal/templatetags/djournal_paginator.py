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
            page = int(self.page.resolve(context))
            pages = self.pages.resolve(context)
            pages_total = len(pages)
            output = ""
            str_list = []
            if pages_total > 1:
                str_list += "<footer class='pagination'>"
                str_list += "<div class='pagination-left'>"
                if page > 1:
                    str_list += "<a class='pagination-left' href='?page=%i'>%s</a>" % (int(page) - 1,_('Previous'))
                else:
                    str_list += "<span class='deactivated'>%s</span>" % _('Previous')
                str_list += "</div>"
                str_list += "<div class='pagination-center'>"
                str_list += "<span class='pagination-center'>%s %s %s %s</span>" % (_('Page'), str(page),_('of'), str(pages_total))
                str_list += "</div>"
                str_list += "<div class='pagination-right'>"
                if page < pages_total:
                    str_list += "<a class='pagination-right' href='?page=%i'>%s</a>" % (int(page) + 1,_('Next'))
                else:
                    str_list += "<span class='deactivated'>%s</span>" % _('Next')
                str_list += "</div>"
                str_list += "</footer>"
            return output.join(str_list)
        except template.VariableDoesNotExist:
            return ''

register = Library()


@register.tag
def djournal_paginator_simple(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(_("Paginator takes two arguments"))
    tagname, pages, page = bits
    return PaginatorSimpleNode(pages, page)

