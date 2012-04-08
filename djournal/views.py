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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from djournal.helpers.date import get_day_name, get_month_name
from djournal.helpers.paginator import paginate
from djournal.models import Entry, Tag
import settings


def entry(request, entry_id):
    variables = dict()
    entry = get_object_or_404(Entry, id=entry_id)
    variables['item'] = entry
    variables['title'] = entry.title
    variables['description'] = entry.description
    t = get_template('djournal/entry.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


def entries_all(request):
    variables = dict()
    variables['title'] = settings.TITLE
    items = Entry.objects.filter(enabled=True).order_by('-modification_date')
    if items:
        page = request.GET.get('page', 1)
        paginate(items, page, variables)        
    else:
        variables['info_enabled'] = True
        variables['info_message'] = _('No Search Results.')
    t = get_template('djournal/entries.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


def entries_day(request, year, month, day):
    variables = dict()
    if year.isdigit() and month.isdigit() and day.isdigit():
        day = int(day)
        year = int(year)
        month = int(month)
        month_name = get_month_name(month)
        day_name = get_day_name(year, month, day)
    else:
        return HttpResponse(status=400)    
    items = Entry.objects.filter(enabled=True, modification_date__month=month, modification_date__year=year, modification_date__day=day).order_by('-modification_date')
    headline = _('Showing results for: %(day)s %(month)s %(year)d') % {'day': day_name, 'month': month_name, 'year': year}
    if items:
        page = request.GET.get('page', 1)
        paginate(items, page, variables)   
        variables['headline'] = headline
    else:
        variables['info_enabled'] = True
        variables['info_message'] = _('No Search Results.')
    t = get_template('djournal/entries.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)



def entries_month(request, year, month):
    variables = dict()
    if year.isdigit() and month.isdigit():
        year = int(year)
        month = int(month)
        month_name = get_month_name(month)
    else:
        return HttpResponse(status=400)
    items = Entry.objects.filter(enabled=True, modification_date__month=month, modification_date__year=year).order_by('-modification_date')
    headline = _('Showing results for: %(month)s %(year)d') % {'month': month_name, 'year': year}
    if items:
        page = request.GET.get('page', 1)
        paginate(items, page, variables)   
        variables['headline'] = headline
    else:
        variables['info_enabled'] = True
        variables['info_message'] = _('No Search Results.')
    t = get_template('djournal/entries.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)



def entries_year(request, year):
    """
    Gets All the Video Post by Date.
    URL: ^date/(?P<page>\d+)/(?P<year>\d{4})/$
    """
    variables = dict()
    if year.isdigit():
        year = int(year)
    else:
        return HttpResponse(status=400)
    items = Entry.objects.filter(enabled=True, modification_date__year=year).order_by('-modification_date')
    headline = _('Showing results for: %(year)d') % {'year': year}
    if items:
        page = request.GET.get('page', 1)
        paginate(items, page, variables)   
        variables['headline'] = headline
    else:
        variables['info_enabled'] = True
        variables['info_message'] = _('No Search Results.')
    t = get_template('djournal/entries.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)


def entries_tag(request, tag_id):
    variables = dict()
    tag_id = int(tag_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    items = tag.entry_set.filter(enabled=True)
    headline = _('Showing results for: %s') % tag.name
    if items:
        page = request.GET.get('page', 1)
        paginate(items, page, variables)   
        variables['headline'] = headline
    else:
        variables['info_enabled'] = True
        variables['info_message'] = _('No Search Results.')
    t = get_template('djournal/entries.html')
    html = t.render(RequestContext(request, variables))
    return HttpResponse(html)

@csrf_exempt
def get_tag_names(request):
    items = Tag.objects.all()
    output = str([str(i.name) for i in items])
    return HttpResponse(output)

