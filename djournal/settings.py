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
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TITLE = getattr(settings, 'BLOG_TITLE', 'BLOG')
SYNDICATION_SUBSCRIBERS = getattr(settings, "SYNDICATION_SUBSCRIBERS", list())
SITEMAP_SUBSCRIBERS = getattr(settings, "SITEMAP_SUBSCRIBERS", list())
CHANGEFREQ = getattr(settings, "SITEMAP_CHANGEFREQ", 'monthly')
PRIORITY = getattr(settings, "SITEMAP_PRIORITY", '0.8')
GENERATOR_DIR = getattr(settings, "SYNDICATION_GENERATOR_DIR", None)
TEMPLATE_DIRS = getattr(settings, "TEMPLATE_DIRS", None)
TEMPLATE_DIRS += (os.path.join(PROJECT_PATH, 'templates'),)
PAGINATOR_MAX_RESULTS = 5