# coding: utf-8
import os.path

if os.path.exists("/etc/DJANGO_DEV_MACHINE"):
    DEVELOPMENT = True
    DEBUG = True
else:
    DEVELOPMENT = False
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ("Andrei AVRAM", "andrei.avram@scout.ro")
)

MANAGERS = ADMINS


if DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'scoutfile3_base',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'sql123.',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            'OPTIONS': {
                        "init_command": "SET foreign_key_checks = 0;",
             },
        }
    }
    
    FILE_ROOT = "/home/yeti/Workspace/scoutfile3/"
    URL_ROOT = "http://localhost/"
    DAJAXICE_MEDIA_PREFIX = "dajaxice"

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'scoutfile3_base',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'me11on_',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            'OPTIONS': {
                        "init_command": "SET foreign_key_checks = 0;",
             },
        }
    }
    
    FILE_ROOT = "/yetiweb/scoutfile/"
    URL_ROOT = "http://projects.albascout.ro/"
    DAJAXICE_MEDIA_PREFIX = "dajaxice"
    

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
MEDIA_ROOT = '%smedia/' % FILE_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '%smedia/scoutfile/' % URL_ROOT

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%sstatic/' % FILE_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '%sstatic/scoutfile/' % URL_ROOT 

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("js", "%sjs" % STATIC_ROOT),
    ("images", "%simages" % STATIC_ROOT),
    ("css", "%scss" % STATIC_ROOT),
    ("font", "%sfont" % STATIC_ROOT),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder'
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^bhel7)sli5=u125nc2a-%$&%ucd)gd-p5@u9cn-o)^w+==jk&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'scoutfile3.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("%stemplates" % FILE_ROOT),
)


TEMPLATE_CONTEXT_PROCESSORS = (
#    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
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
    'ajax_select', "tagging", 'pagination', 'less',
    
    'scoutfile3.structuri', 'scoutfile3.generic', 'scoutfile3.album',
    'scoutfile3.patrocle', 'scoutfile3.documente',  
)


AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'membri'     : ('scoutfile3.structuri.lookups', 'MembriLookup')
}

AJAX_SELECT_BOOTSTRAP = False
AJAX_SELECT_INLINES = False


#if DEVELOPMENT:
#    INSTALLED_APPS += ("debug_toolbar", )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
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
        
        'django.db.backends' : {
            'handlers' : ['null', ], 
            'propagate' : False,
            'level': 'DEBUG',
        }        
            
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

SYSTEM_EMAIL = "sistem@scout.ro"
SERVER_EMAIL = "sistem@scout.ro"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "sistem@scout.ro"
EMAIL_HOST_PASSWORD = "yetiRulz1_"
EMAIL_USE_TLS = True

if DEVELOPMENT:
    RECAPTCHA_PUBLIC_KEY = '6Leo2boSAAAAAMs0TyrzCbEEral5RbTs3qOKpws8'
    RECAPTCHA_PRIVATE_KEY = '6Leo2boSAAAAAJpxCUHYB6B1I1sDvZqFL1_dtwlh'
else:
    RECAPTCHA_PUBLIC_KEY = '6Ld1_tUSAAAAADX2GeFK7g56q9EE3dz5OZX99FOi'
    RECAPTCHA_PRIVATE_KEY = '6Ld1_tUSAAAAAHZTsyehDAEmvlacDimNomNCLGyo'

RECAPTCHA_USE_SSL = True
USE_EMAIL_CONFIRMATION = False

LESS_OUTPUT_DIR = "less_cache"

SMSLINK_URL = "http://www.smslink.ro/sms/gateway/communicate/"
SMSLINK_CONNID = "A196357A18017C10"
SMSLINK_PASSWORD = "yetiRulz1_"

REDMINE_API_KEY = "f393aac0746069a9de25eb251b0171b1ff1ed793"

VALOARE_IMPLICITA_COTIZATIE_LOCAL = 0
VALOARE_IMPLICITA_COTIZATIE_NATIONAL = 50