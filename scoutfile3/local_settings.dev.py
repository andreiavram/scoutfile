DEVELOPMENT = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG


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

URL_ROOT = "http://testing.albascout.ro/"
    
RECAPTCHA_PUBLIC_KEY = '6LfvEugSAAAAACYg-ROb497cATzGXOHTsRWq8Obl'
RECAPTCHA_PRIVATE_KEY = '6LfvEugSAAAAADwOHOGrxbOB7rErb0KGAsgUzkak'
RECAPTCHA_USE_SSL = True
USE_EMAIL_CONFIRMATION = False

RAVEN_CONFIG = {
    'dsn': 'http://d7e2875a012341e592603b37604c5728:ebf178b496c54a73a536c5e79d7eeff5@sentry.albascout.ro/5',
}