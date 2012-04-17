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
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from djournal.helpers import signals

class Tag(models.Model):
    ORDER_VALUES = {
        0: ("-name", _('Name')),
    }
    name = models.CharField(unique=True, max_length=50, verbose_name=_('Name'), null=False, blank=False)    
    slug = models.SlugField(max_length=50, verbose_name=_('Slug'), null=True, blank=True, unique=True)
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
        0: ("-modification_date", _('Newest first')),
        1: ("modification_date", _('Older first')),
        2: ("title", _('Title')),
    }
    title = models.CharField(max_length=250, verbose_name=_('Title'), unique=True, null=False, blank=False)    
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    content = models.TextField(verbose_name=_('Content'), null=False, blank=False)
    enabled = models.BooleanField(verbose_name=_('Enabled'), default=True)
    slug = models.SlugField(max_length=250, verbose_name=_('Slug'), null=True, blank=True, unique=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tag'), null=True, blank=True)
    @models.permalink
    def get_absolute_url(self):
        return ('djournal-entry', [self.id, self.slug])
    def __unicode__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

post_delete.connect(signals.generation_signal, sender=Entry)
post_save.connect(signals.generation_signal, sender=Entry)
post_delete.connect(signals.generation_signal, sender=Tag)
post_save.connect(signals.generation_signal, sender=Tag)
