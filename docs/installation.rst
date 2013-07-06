.. djournal documentation master file, created by
   sphinx-quickstart on Mon Jul  1 16:36:52 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Djournal installation
=====================

Set a Django Project 
--------------------

1) Blank blog

::

    django-admin.py startproject blankproject

Edit the settings
-----------------
::

    import os
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    PROJECT_PARENT_PATH = os.path.abspath(os.path.join(PROJECT_PATH, "../"))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 
            'NAME': 'blankproject',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        '/path/to/djournal/static',
    )
    TEMPLATE_DIRS = (
             os.path.join(PROJECT_PATH, 'templates/'),
    )
    
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.sitemaps',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'djournal',
        'django.contrib.admin',
    )

urls.py
-------
::

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


Create the tables
-----------------
::

    python manage.py syncdb


