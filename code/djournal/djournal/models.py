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
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from djournal.helpers import signals


class Tag(models.Model):
    ORDER_VALUES = {
        0: ("-name", _('Name')),
    }
    name = models.CharField(max_length=50, verbose_name=_('Name'), blank=False, unique=True)
    slug = models.SlugField(max_length=50, verbose_name=_('Slug'), blank=True, unique=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('djournal-entries-tag', [self.id, self.slug])

    def get_slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Entry(models.Model):
    ORDER_VALUES = {
        0: ("-creation_date", _('Newest first')),
        1: ("creation_date", _('Older first')),
        2: ("title", _('Title')),
    }
    title = models.CharField(max_length=250, verbose_name=_('Title'), unique=False, blank=False)
    excerpt = models.TextField(verbose_name=_('Excerpt'), blank=True)
    content = models.TextField(verbose_name=_('Content'), blank=False)
    published = models.BooleanField(verbose_name=_('Published'), default=False)
    featured = models.BooleanField(verbose_name=_('Featured'), default=False)
    description = models.TextField(verbose_name=_('Meta Description'), blank=True)
    keywords = models.TextField(verbose_name=_('Meta Keywords'), blank=True)
    slug = models.SlugField(max_length=250, verbose_name=_('Slug'), blank=True, unique=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    start_publication = models.DateTimeField(verbose_name=_('Start Publication'), null=True, blank=True,)
    end_publication = models.DateTimeField(verbose_name=_('End Publication'), null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tag'), null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('djournal-entry', [self.id, self.slug])

    @models.permalink
    def get_permalink_url(self):
        return ('djournal-entry-permalink', [self.id,])

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        permissions = (
            ("edit_all_entries", "Can edit all the entries."),
        )
        ordering = ['-creation_date']

post_delete.connect(signals.clean_cache_signal, sender=Entry)
post_save.connect(signals.clean_cache_signal, sender=Entry)
post_delete.connect(signals.clean_cache_signal, sender=Tag)
post_save.connect(signals.clean_cache_signal, sender=Tag)
