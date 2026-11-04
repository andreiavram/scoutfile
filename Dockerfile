# Scoutfile production image (Coolify). Python 3.10 = the EC2 host's Ubuntu 22.04 interpreter,
# and the newest one numpy==1.22.0 ships wheels for.
FROM python:3.10-slim-bookworm AS build

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY deploy/requirements.txt deploy/docker/constraints.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip -c /tmp/constraints.txt setuptools \
 && pip install --no-cache-dir -r /tmp/requirements.txt -c /tmp/constraints.txt


FROM python:3.10-slim-bookworm

# GDAL/GEOS/PROJ for django.contrib.gis; static and media are served from S3 + CloudFront.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 libgdal32 libgeos-c1v5 libproj25 libjpeg62-turbo zlib1g libxml2 libxslt1.1 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=scoutfile3.settings_docker

RUN useradd --create-home --uid 1000 app
COPY --chown=app:app . /app
RUN mkdir -p /app/logs /app/keys && chown app:app /app/logs /app/keys \
 && chmod +x /app/deploy/docker/entrypoint.sh

USER app
WORKDIR /app/web

# Fails the build on a broken import or a missing GDAL/GEOS, not the first request.
RUN SCOUTFILE_BUILD_CHECK=1 python manage.py check && rm -rf /app/media

EXPOSE 8000
ENTRYPOINT ["/app/deploy/docker/entrypoint.sh"]
CMD ["web"]
