DEVELOPMENT = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'scoutfile_local',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '"root123."',                  # Not used with sqlite3.
        'HOST': 'mysql',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            },
        }
}

RECAPTCHA_PUBLIC_KEY = '6Le0EugSAAAAAC1d92CTxm9ZS-7rFeM-cd-24uTU'
RECAPTCHA_PRIVATE_KEY = '6Le0EugSAAAAAGDT2cAH3ybOhxGqY4w2ZnYCJOAZ'
RECAPTCHA_USE_SSL = True
USE_EMAIL_CONFIRMATION = False

RAVEN_CONFIG = {
    'dsn': 'http://d7e2875a012341e592603b37604c5728:ebf178b496c54a73a536c5e79d7eeff5@sentry.albascout.ro/5',
}

URL_ROOT = "http://127.0.0.1:8000"

AWS_ACCESS_KEY_ID = "AKIAJA5OORXJQPQHSYOQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = 'scoutfile-local'
S3_URL = 'http://%s.s3-website-eu-west-1.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_DIRECTORY = 'media/'
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

SMSLINK_URL = "http://www.smslink.ro/sms/gateway/communicate/"
SMSLINK_CONNID = "A196357A18017C10"
SMSLINK_PASSWORD = ""

BOWER_PATH = '/usr/bin/bower'

ONCR_USER = "andrei.avram@albascout.ro"
ONCR_PASSWORD = ""

GATEKEEPER_CONNECTION_STRING = "pi@10.8.0.10"
GATEKEEPER_CONNECTION_PASSWORD = "raspberry"

REMOTE_DB = {
    "name": "scoutfile3_production",
    "user": "root",
    "password": "sql123.",
    "host": "yeti.albascout.ro",
    "ssh_host": "lair",
    "ssh_user": "yeti",
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached',
    },
    'redis': {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    },
}