from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from djournal.views import entries_all
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djournaltest.views.home', name='home'),
    # url(r'^djournaltest/', include('djournaltest.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^blog/', include('djournal.urls')),
    url(r'^$', entries_all, name='djournalsite-index'),   
)
