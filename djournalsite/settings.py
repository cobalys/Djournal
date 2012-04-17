import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PARENT_PATH = os.path.abspath(os.path.join(PROJECT_PATH,".."))

try:
    import djournalsite.settings_local
    DATABASES = djournalsite.settings_local.DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'djournal', 
            'USER': '',
            'PASSWORD': '', 
            'HOST': '',
            'PORT': '', 
        }
    }

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PARENT_PATH, 'djournal-media/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'hk4yr9h8t2+3y!5+jrmq+#7f5x9g6pqwuge&r!-5(l=sf*m(pf'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'djournalsite.urls'

TEMPLATE_DIRS = (
                 os.path.join(PROJECT_PATH, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'djournal',
    'django.contrib.admin',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


DJOURNAL_GENERATOR_DIR = os.path.join(PROJECT_PATH, 'templates/cache/')
DJOURNAL_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"
DJOURNAL_JQUERYUI_URL = "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.18/jquery-ui.min.js"