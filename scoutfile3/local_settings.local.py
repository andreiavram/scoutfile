DEVELOPMENT = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'scoutfile3',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'sql123.',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
                    "init_command": "SET foreign_key_checks = 0;",
         },
    }
}

# DAJAXICE_MEDIA_PREFIX = "dajaxice"

RECAPTCHA_PUBLIC_KEY = '6Le0EugSAAAAAC1d92CTxm9ZS-7rFeM-cd-24uTU'
RECAPTCHA_PRIVATE_KEY = '6Le0EugSAAAAAGDT2cAH3ybOhxGqY4w2ZnYCJOAZ'
RECAPTCHA_USE_SSL = True
USE_EMAIL_CONFIRMATION = False

# MEDIA_ROOT = "/vagrant/media/"
# STATIC_ROOT = "/vagrant/static/"

RAVEN_CONFIG = {
    'dsn': 'http://d7e2875a012341e592603b37604c5728:ebf178b496c54a73a536c5e79d7eeff5@sentry.albascout.ro/5',
}

URL_ROOT = "http://192.168.33.10:8000"

AWS_ACCESS_KEY_ID="AKIAJ5CUJA364SCHQJOQ"
AWS_SECRET_ACCESS_KEY="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"
AWS_STORAGE_BUCKET_NAME = 'scoutfile'
S3_URL = 'http://%s.s3-website-eu-west-1.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_DIRECTORY = 'media/'
MEDIA_URL = S3_URL + MEDIA_DIRECTORY