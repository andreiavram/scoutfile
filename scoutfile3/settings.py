# coding: utf-8
import os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ("Andrei AVRAM", "andrei.avram@albascout.ro")
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Bucharest'
LANGUAGE_CODE = 'ro-ro'
USE_I18N = True
USE_L10N = True

SITE_ID = 1


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'scoutfile3.s3utils.MediaS3BotoStorage'
LOCAL_MEDIA_ROOT = os.path.join(BASE_DIR, "media")
LOCAL_MEDIA_URL = "/media/"


STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    ("js", os.path.join(STATIC_ROOT, "js")),
    ("images", os.path.join(STATIC_ROOT, "images")),
    ("css", os.path.join(STATIC_ROOT, "css")),
    ("font", os.path.join(STATIC_ROOT, "font")),
    ("jquery_upload", os.path.join(STATIC_ROOT, "jquery_upload")),
    ("gallery", os.path.join(STATIC_ROOT, "gallery")),
    ("bootstrap-calendar", os.path.join(STATIC_ROOT, "bootstrap-calendar")),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)


SECRET_KEY = '^bhel7)sli5=u125nc2a-%$&%ucd)gd-p5@u9cn-o)^w+==jk&'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    'scoutfile3.middleware.ImpersonateUserMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'redis': {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "127.0.0.1:6379",
        "OPTIONS": {
            "DB": 1,
        }
    },
}

ROOT_URLCONF = 'scoutfile3.urls'

TEMPLATE_DIRS = (
    (os.path.join(BASE_DIR, "scoutfile3", "templates")),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'scoutfile3.context_processors.product_version',
    'scoutfile3.context_processors.api_keys',
    'scoutfile3.context_processors.url_root',
)


INTERNAL_IPS = ("192.168.33.1", "127.0.0.1", "95.77.249.243")
ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'redis_cache',

    #   django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    #   third party pluggables
    'debug_toolbar',
    'photologue',
    'crispy_forms',
    'rest_framework',
    'captcha',
    'ajax_select',
    "taggit",
    'pagination_bootstrap',
    'less',
    'raven.contrib.django.raven_compat',
    'django_extensions',
    'gunicorn',
    'djangobower',
    'longerusername',
    'storages',
    'django_markdown',
    'django_ace',
    'qrcode',

    #   ecosystem apps
    'goodies',

    #   internal scoutfile3 apps
    'structuri',
    'generic',
    'album',
    'patrocle',
    'documente',
    'extra',
    'utils',
    'proiecte',
    'cantece',
    'jocuri',
    'badge',
    'adrese_postale',
    'inventar',
)

WSGI_APPLICATION = 'scoutfile3.wsgi.application'

# AJAX_LOOKUP_CHANNELS = {
#     'membri': ('structuri.lookups', 'MembriLookup'),
#     'lideri': ('structuri.lookups', 'LideriLookup'),
# }

AJAX_SELECT_BOOTSTRAP = False
AJAX_SELECT_INLINES = False

# TODO: move logging settings to its own module
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry'],
        },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': "%s/logs/debug.log" % BASE_DIR,
            'formatter': 'verbose',
            },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '%s/logs/error.log' % BASE_DIR,
            'formatter': 'verbose',
            },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
            },
        'sentry': {
            'level': 'ERROR',
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
            'level': 'DEBUG',
            },

        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
            },

        'django.db.backends': {
            'handlers': ['null', ],
            'propagate': False,
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
FIXTURE_DIRS = ["%s/fixtures" % BASE_DIR, ]


LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/edit/"

# TODO: remove secrets from here
SYSTEM_EMAIL = "sistem@albascout.ro"
SERVER_EMAIL = "sistem@albascout.ro"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "sistem@albascout.ro"
EMAIL_HOST_PASSWORD = "yetiRulz1_"
EMAIL_USE_TLS = True


LESS_OUTPUT_DIR = "less_cache"


VALOARE_IMPLICITA_COTIZATIE_LOCAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL = 50
VALOARE_IMPLICITA_COTIZATIE_LOCAL_SOCIAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL_SOCIAL = 12


SCOUTFILE_ALBUM_STORAGE_ROOT = "album"
def photologue_path(instance, filename):
    return os.path.join(SCOUTFILE_ALBUM_STORAGE_ROOT, filename)
PHOTOLOGUE_PATH = photologue_path

from scoutfile3.version import *

DATE_INPUT_FORMATS = ('%d.%m.%Y', ) + global_settings.DATE_INPUT_FORMATS
DATETIME_INPUT_FORMATS = ('%d.%m.%Y %H:%M %p', '%d.%m.%Y %H:%M:%S') + global_settings.DATETIME_INPUT_FORMATS

# TODO: remove secrets from here
GOOGLE_API_KEY = "AIzaSyCIiQgKmmRv2SLBj8KTbx6HB7Kn_6LIU-o"


# TODO: remove secrets from here
FACEBOOK_LOGIN_REDIRECT = "login"
FACEBOOK_APP_ID = "152554668279442"
FACEBOOK_APP_SECRET = "388c926e843601ac88f16274923245ea"
FACEBOOK_PERMISSIONS = ['email', ]
FACEBOOK_ERROR_URL = "login"

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'utils.auth_backends.FacebookBackend',)

CRISPY_TEMPLATE_PACK = "bootstrap"
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, "components")
BOWER_PATH = '/usr/bin/bower'

BOWER_INSTALLED_APPS = ('lodash#3.2.0',
 'bootstrap#2.3.2',
 'jquery#1.10.2',
 'moment#2.0.0',
 'bootstrap-calendar#0.2.4',
 'jquery-cookie#1.4.1')

CENTRU_LOCAL_IMPLICIT = 1
REDMINE_APY_KEY = ""


from pyembed.markdown import PyEmbedMarkdown
from utils.mdextend import scoutfile as scoutfile_markdown
MARKDOWN_EXTENSIONS = ['extra', PyEmbedMarkdown(), scoutfile_markdown.makeExtension()]  # iconfonts.makeExtension()]

MARKDOWN_STYLE = os.path.join(STATIC_ROOT, "css", "markdown-preview.css")
MARKDOWN_EDITOR_SKIN = 'simple'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

from local_settings import *