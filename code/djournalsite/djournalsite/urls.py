from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from djournal.sitemap import DjournalSitemap
from djournal.views import entries_all
admin.autodiscover()

sitemaps = {
    'djournal': DjournalSitemap,
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('djournal.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^$', entries_all, name='djournalsite-index'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            url(r'^media/djournalsite/(?P<path>.*)$',
                'django.views.static.serve',
                {
                 'document_root': settings.MEDIA_ROOT,
                }
                ),
    )
