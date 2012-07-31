from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from djournal.views import entries_all
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('djournal.urls')),
    url(r'^$', entries_all, name='djournalsite-index'),   
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            url(r'^media/cobalys/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
            }),
    )
