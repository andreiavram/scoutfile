DEVELOPMENT = False
DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'scoutfile3_production',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'me11on_',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
                    "init_command": "SET foreign_key_checks = 0;",
         },
    }
}

URL_ROOT = "http://scoutfile.albascout.ro/"
# DAJAXICE_MEDIA_PREFIX = "dajaxice"
    
RECAPTCHA_PUBLIC_KEY = '6Ld1_tUSAAAAADX2GeFK7g56q9EE3dz5OZX99FOi'
RECAPTCHA_PRIVATE_KEY = '6Ld1_tUSAAAAAHZTsyehDAEmvlacDimNomNCLGyo'
RECAPTCHA_USE_SSL = True
USE_EMAIL_CONFIRMATION = False


RAVEN_CONFIG = {
    'dsn': 'http://cce06e32cfae4025af7c2b39b889bc27:79ab9be2ff1e428babc298166b5ad9f5@sentry.albascout.ro/2',
}