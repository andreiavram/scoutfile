# coding: utf-8
"""Settings for the container image (Coolify).

Layered on top of ``settings`` — which still imports ``local_settings`` — so the production
``local_settings.py`` keeps working unchanged: the entrypoint writes it from
``SCOUTFILE_LOCAL_SETTINGS_B64``. Only what differs inside a container is overridden here:
the database, cache and broker hosts, logging to stdout, and running behind Traefik.
"""
import os

from .settings import *  # noqa: F401,F403


def env_list(name):
    return [item.strip() for item in os.environ.get(name, "").split(",") if item.strip()]


# settings.py declares ADMINS as one bare pair (no trailing comma); AdminEmailHandler then
# raises inside the 500 handler and the error mail is never sent.
if ADMINS and isinstance(ADMINS[0], str):  # noqa: F405
    ADMINS = [ADMINS]  # noqa: F405
MANAGERS = ADMINS

DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
TEMPLATE_DEBUG = DEBUG

if os.environ.get("DJANGO_SECRET_KEY"):
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

if env_list("DJANGO_ALLOWED_HOSTS"):
    ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")

# Traefik terminates TLS and passes X-Forwarded-Proto straight to gunicorn.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{host.lstrip('.')}" for host in ALLOWED_HOSTS if host != "*"]

# The container healthcheck probes by IP; django_hosts sends it to the default host.
ALLOWED_HOSTS = [*ALLOWED_HOSTS, "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("POSTGRES_DB", "scoutfile"),
        "USER": os.environ.get("POSTGRES_USER", "scoutfile"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "scoutfile-db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

# The image build's `manage.py check` has none of production's local_settings: photologue calls
# default_storage.exists() at import time, which needs S3 credentials, and django-recaptcha
# errors on its test keys. Never set it on a running app.
if os.environ.get("SCOUTFILE_BUILD_CHECK") == "1":
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

CACHES["default"]["LOCATION"] = os.environ.get("MEMCACHED_LOCATION", "scoutfile-memcached:11211")  # noqa: F405
CACHES["redis"]["LOCATION"] = os.environ.get("REDIS_CACHE_URL", "redis://scoutfile-redis:6379/1")  # noqa: F405
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://scoutfile-redis:6379/0")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "root": {"handlers": ["console"], "level": os.environ.get("LOG_LEVEL", "INFO")},
    "loggers": {
        "django.request": {"handlers": ["mail_admins"], "level": "ERROR", "propagate": True},
        "django.db.backends": {"level": "INFO"},
        # Scanners probing by IP or a stray Host would otherwise mail ADMINS on every request.
        "django.security.DisallowedHost": {"handlers": [], "propagate": False},
    },
}
