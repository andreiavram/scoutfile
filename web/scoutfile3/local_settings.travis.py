DEVELOPMENT = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
USE_EMAIL_CONFIRMATION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # Or path to database file if using sqlite3.
        'USER': 'travis',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            },
        }
}

URL_ROOT = "http://scoutfile.albascout.ro/"

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = True

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = 'scoutfile-'
S3_URL = 'http://%s.s3-website-eu-west-1.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_DIRECTORY = 'media/'
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

SMSLINK_URL = "http://www.smslink.ro/sms/gateway/communicate/"
SMSLINK_CONNID = ""
SMSLINK_PASSWORD = ""

REDMINE_API_KEY = ""
BOWER_PATH = "/usr/local/bin/bower"

ONCR_USER = "andrei.avram@albascout.ro"
ONCR_PASSWORD = ""

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'