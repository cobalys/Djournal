from django.contrib.sitemaps import Sitemap
from django.core.cache import cache
from djournal.models import Entry


class DjournalSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        entries_sitemap = cache.get('djournal_entries_sitemap')
        if not entries_sitemap:
            entries_sitemap = Entry.objects.filter(enabled=True)
            cache.set('djournal_entries_sitemap', entries_sitemap)
        return entries_sitemap

    def lastmod(self, obj):
        return obj.modification_date
