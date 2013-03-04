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

# DAJAXICE_MEDIA_PREFIX = "dajaxice"

RECAPTCHA_PUBLIC_KEY = '6Leo2boSAAAAAMs0TyrzCbEEral5RbTs3qOKpws8'
RECAPTCHA_PRIVATE_KEY = '6Leo2boSAAAAAJpxCUHYB6B1I1sDvZqFL1_dtwlh'
RECAPTCHA_USE_SSL = True
USE_EMAIL_CONFIRMATION = False
