# coding: utf-8
import os.path

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ("Andrei AVRAM", "andrei.avram@albascout.ro")
)

MANAGERS = ADMINS


components = os.path.abspath(__file__).split(os.sep)[:-2]
FILE_ROOT = str.join(os.sep, components)

from local_settings import *

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bucharest'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ro-ro'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/media/' % FILE_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%s/static/' % FILE_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' 

# Additional locations of static files
STATICFILES_DIRS = (
    ("js", "%s/js" % STATIC_ROOT),
    ("images", "%s/images" % STATIC_ROOT),
    ("css", "%s/css" % STATIC_ROOT),
    ("font", "%s/font" % STATIC_ROOT),
    ("jquery_upload", "%s/jquery_upload" % STATIC_ROOT),
    ("gallery", os.path.join(STATIC_ROOT, "gallery")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder'
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^bhel7)sli5=u125nc2a-%$&%ucd)gd-p5@u9cn-o)^w+==jk&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("%s/templates" % FILE_ROOT),
)


TEMPLATE_CONTEXT_PROCESSORS = (
#    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'context_processors.product_version',
    'context_processors.api_keys',
    'context_processors.url_root',
)

#if DEVELOPMENT:
#    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    
    'south', 'photologue',
    'dajax', 'dajaxice',
    'crispy_forms', 'djangorestframework', 'captcha',
    'ajax_select', "taggit", 'pagination', 'less',
    
    'structuri', 'generic', 'album',
    'patrocle', 'documente', 'extra',
    "utils",
    
    'raven.contrib.django.raven_compat',
    'django_extensions', 'gunicorn', 'goodies',
)


AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'membri'     : ('structuri.lookups', 'MembriLookup')
}

AJAX_SELECT_BOOTSTRAP = False
AJAX_SELECT_INLINES = False

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'root' : {
    #   'level' : 'WARNING',
    #   'handlers' : ['sentry'],
    # },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },    
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level' : 'DEBUG',
            'class': 'logging.FileHandler',
            'filename' : "%s/logs/debug.log" % FILE_ROOT,
            'formatter' : 'verbose',
        },
        'error' : {
            'level' : 'ERROR',
            'class' : 'logging.FileHandler',
            'filename' : '%s/logs/error.log' % FILE_ROOT,
            'formatter' : 'verbose',
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'sentry' : {
            'level' : 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        
        '': {
            'handlers': ['default'],
            'propagate': True,
            'level':'DEBUG',
        },

        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
        
        'django.db.backends' : {
            'handlers' : ['null', ], 
            'propagate' : False,
            'level': 'DEBUG',
        },

       'raven': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
            
    }
}


PHOTOLOGUE_DIR = "poze"
PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH = 1024
FIXTURE_DIRS = ["%s/fixtures" % FILE_ROOT, ]

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#        'URL': 'http://127.0.0.1:9200/',
#        'INDEX_NAME': 'haystack',
#    },
#}

AUTH_PROFILE_MODULE = 'structuri.Utilizator'
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/edit/"

SYSTEM_EMAIL = "sistem@albascout.ro"
SERVER_EMAIL = "sistem@albascout.ro"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "sistem@albascout.ro"
EMAIL_HOST_PASSWORD = "yetiRulz1_"
EMAIL_USE_TLS = True


LESS_OUTPUT_DIR = "less_cache"

SMSLINK_URL = "http://www.smslink.ro/sms/gateway/communicate/"
SMSLINK_CONNID = "A196357A18017C10"
SMSLINK_PASSWORD = "yetiRulz1_"

REDMINE_API_KEY = "f393aac0746069a9de25eb251b0171b1ff1ed793"

VALOARE_IMPLICITA_COTIZATIE_LOCAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL = 50
VALOARE_IMPLICITA_COTIZATIE_LOCAL_SOCIAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL_SOCIAL = 12


SCOUTFILE_ALBUM_STORAGE_ROOT = "album"

from version import *

DATE_INPUT_FORMATS = (
    '%d.%m.%Y',
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
)

DATETIME_INPUT_FORMATS = (
    '%d.%m.%Y %H:%M %p',
    '%d.%m.%Y %H:%M:%S',
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
)

GOOGLE_API_KEY = "AIzaSyCIiQgKmmRv2SLBj8KTbx6HB7Kn_6LIU-o"

FACEBOOK_LOGIN_REDIRECT = "login"    #  url reverse-able string
FACEBOOK_APP_ID = "152554668279442"
FACEBOOK_APP_SECRET = "388c926e843601ac88f16274923245ea"
FACEBOOK_PERMISSIONS = ['email', 'publish_stream']
FACEBOOK_ERROR_URL = "login"

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                           'utils.auth_backends.FacebookBackend',
)

