# coding: utf-8
from __future__ import absolute_import
import os
from django.conf import global_settings
from django.utils.translation import gettext_lazy as _

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Andrei AVRAM", "andrei.avram@albascout.ro")
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Bucharest'
LANGUAGE_CODE = 'ro'

LANGUAGES = [
    ('ro', _('Romanian')),
    ('en', _('English')),
]

USE_I18N = True
USE_L10N = True

SITE_ID = 1


MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATICFILES_STORAGE = 'scoutfile3.s3utils.StaticFilesStorage'
MEDIAFILES_STORAGE = 'scoutfile3.s3utils.MediaFilesStorage'

AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False

LOCAL_MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
LOCAL_MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
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
    'django_yarnpkg.finders.NodeModulesFinder',
)

NODE_MODULES_ROOT = os.path.join(PROJECT_ROOT, 'node_modules')

SECRET_KEY = '^bhel7)sli5=u125nc2a-%$&%ucd)gd-p5@u9cn-o)^w+==jk&'

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_pagination_bootstrap.middleware.PaginationMiddleware",
    'scoutfile3.middleware.ImpersonateUserMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware'
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'redis': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

ROOT_URLCONF = 'scoutfile3.urls'
ROOT_HOSTCONF = 'scoutfile3.hosts'
DEFAULT_HOST = "scoutfile"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "scoutfile3" / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'scoutfile3.context_processors.product_version',
                'scoutfile3.context_processors.api_keys',
                'scoutfile3.context_processors.url_root',
            ],
        },
    },
]


INTERNAL_IPS = ("192.168.33.1", "127.0.0.1", "95.77.249.243")
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django_redis',

    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    #   third party pluggables
    'photologue',
    'crispy_forms',
    'rest_framework',
    'rest_framework_sso',
    'captcha',
    'ajax_select',
    "taggit",
    'django_pagination_bootstrap',
    # "bootstrap_pagination",
    # 'less',
    # 'raven.contrib.django.raven_compat',
    'django_extensions',
    'gunicorn',
    # 'djangobower',
    'django_yarnpkg',
    # 'longerusername', this is out
    'storages',
    # 'django_markdown',
    'django_ace',
    'qrcode',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    "wagtail.contrib.table_block",
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',

    'modelcluster',

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
    'pages',

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
        'handlers': ['default'],
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
            'filename': "%s/logs/debug.log" % PROJECT_ROOT,
            'formatter': 'verbose',
            },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '%s/logs/error.log' % PROJECT_ROOT,
            'formatter': 'verbose',
            },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            },
        # 'sentry': {
        #     'level': 'ERROR',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        #     },
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SYSTEM_EMAIL = "sistem@albascout.ro"
SERVER_EMAIL = "sistem@albascout.ro"
EMAIL_HOST =     "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "sistem@albascout.ro"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

# django_less doesn't do well with python3
# LESS_OUTPUT_DIR = "less_cache"


VALOARE_IMPLICITA_COTIZATIE_LOCAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL = 50
VALOARE_IMPLICITA_COTIZATIE_LOCAL_SOCIAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL_SOCIAL = 12


SCOUTFILE_ALBUM_STORAGE_ROOT = "album"
def photologue_path(instance, filename):
    return os.path.join(SCOUTFILE_ALBUM_STORAGE_ROOT, filename)
PHOTOLOGUE_PATH = photologue_path


DATE_INPUT_FORMATS = ['%d.%m.%Y', ] + list(global_settings.DATE_INPUT_FORMATS)
DATETIME_INPUT_FORMATS = ['%d.%m.%Y %H:%M %p', '%d.%m.%Y %H:%M:%S'] + list(global_settings.DATETIME_INPUT_FORMATS)

# TODO: remove secrets from here
GOOGLE_API_KEY = ""


# TODO: remove secrets from here
FACEBOOK_LOGIN_REDIRECT = "login"
FACEBOOK_APP_ID = "152554668279442"
FACEBOOK_APP_SECRET = "388c926e843601ac88f16274923245ea"
FACEBOOK_PERMISSIONS = ['email', ]
FACEBOOK_ERROR_URL = "login"

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'utils.auth_backends.FacebookBackend',)

CRISPY_TEMPLATE_PACK = "bootstrap"
BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, "components")


YARN_INSTALLED_APPS = ('lodash@3.2.0',
 'bootstrap@3.4.1',
 'jquery@3.6.0',
 'moment@2.0.0',
 'bootstrap-calendar@0.2.4',
 'js-cookie@3.0.1')

CENTRU_LOCAL_IMPLICIT = 1
REDMINE_APY_KEY = ""

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# from pyembed.markdown import PyEmbedMarkdown
# from utils.mdextend import scoutfile as scoutfile_markdown

# MARKDOWN_EXTENSIONS = ['extra', PyEmbedMarkdown(), scoutfile_markdown.makeExtension()]  # iconfonts.makeExtension()]

# MARKDOWN_STYLE = os.path.join(STATIC_ROOT, "css", "markdown-preview.css")
# MARKDOWN_EDITOR_SKIN = 'simple'

# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_sso.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

REST_FRAMEWORK_SSO = {
    'CREATE_AUTHORIZATION_PAYLOAD': 'utils.authentication.create_authorization_payload',
    # 'AUTHENTICATE_PAYLOAD': 'utils.authentication.authenticate_payload',
    'IDENTITY': 'scoutfile',
    'SESSION_AUDIENCE': ['scoutfile', ],
    'AUTHORIZATION_AUDIENCE': ['scoutfile', 'organizer', 'geogame'],
    'ACCEPTED_ISSUERS': ['scoutfile'],
    'KEY_STORE_ROOT': PROJECT_ROOT / 'keys',
    'PUBLIC_KEYS': {
        'scoutfile': ['scoutfile-2023.pem']
    },
    'PRIVATE_KEYS': {
        'scoutfile': ['scoutfile-2023.pem']
    }
}


#   from django 3.2 config
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# WAGTAIL SETTINGS

# This is the human-readable name of your Wagtail install
# which welcomes users upon login to the Wagtail admin.
WAGTAIL_SITE_NAME = 'Scoutfile'

# Replace the search backend
#WAGTAILSEARCH_BACKENDS = {
#  'default': {
#    'BACKEND': 'wagtail.search.backends.elasticsearch5',
#    'INDEX': 'myapp'
#  }
#}

# Wagtail email notifications from address
# WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'wagtail@myhost.io'

# Wagtail email notification format
# WAGTAILADMIN_NOTIFICATION_USE_HTML = True

# Reverse the default case-sensitive handling of tags
TAGGIT_CASE_INSENSITIVE = True


try:
    from scoutfile3.local_settings import *
except ImportError as e:
    pass


try:
    from .version import *
except ImportError:
    pass
