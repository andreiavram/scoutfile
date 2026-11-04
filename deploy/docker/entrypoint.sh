#!/bin/sh
# One image, three roles: web | worker | migrate (anything else runs as a manage.py command).
set -eu

cd /app/web

# The production local_settings.py and the JWT signing key are not in the repo; Coolify holds
# them as base64 env vars so they survive redeploys without a host file mount.
if [ -n "${SCOUTFILE_LOCAL_SETTINGS_B64:-}" ]; then
    echo "$SCOUTFILE_LOCAL_SETTINGS_B64" | base64 -d > /app/web/scoutfile3/local_settings.py
fi
if [ -n "${SCOUTFILE_JWT_KEY_B64:-}" ]; then
    echo "$SCOUTFILE_JWT_KEY_B64" | base64 -d > /app/keys/scoutfile-2023.pem
    chmod 600 /app/keys/scoutfile-2023.pem
fi

role="${1:-web}"
if [ "$#" -gt 0 ]; then
    shift
fi

case "$role" in
    web)
        exec gunicorn scoutfile3.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers "${GUNICORN_WORKERS:-2}" \
            --threads "${GUNICORN_THREADS:-4}" \
            --timeout "${GUNICORN_TIMEOUT:-120}" \
            --access-logfile - \
            --forwarded-allow-ips "*"
        ;;
    worker)
        exec celery -A scoutfile3 worker \
            --queues celery,process_slack_messages \
            --concurrency "${CELERY_CONCURRENCY:-1}" \
            --loglevel INFO
        ;;
    migrate)
        # A fresh database must get the production dump first: migrating it would create an
        # empty schema that pg_restore then collides with. So on an empty database, skip.
        # Exit 3 means "empty"; any other failure (database unreachable) fails the deploy.
        status=0
        python manage.py shell -c "from django.db import connection; import sys; sys.exit(0 if 'django_migrations' in connection.introspection.table_names() else 3)" || status=$?
        if [ "$status" -eq 3 ]; then
            echo "migrate: the database has no django_migrations table — restore the production dump, then redeploy."
            exit 0
        fi
        [ "$status" -eq 0 ] || exit "$status"
        exec python manage.py migrate --noinput
        ;;
    *)
        exec python manage.py "$role" "$@"
        ;;
esac
