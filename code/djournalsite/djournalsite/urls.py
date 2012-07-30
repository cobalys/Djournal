from django.conf.urls.defaults import patterns, include, url
from djournal.views import entries_all
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('djournal.urls')),
    url(r'^$', entries_all, name='djournalsite-index'),   
)
