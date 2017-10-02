FROM django:1.8.7-python2

RUN apt-get update && apt-get install -y \
    git-core \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    ttf-dejavu \
 && rm -rf /var/lib/apt/lists

RUN pip install --upgrade pip
RUN pip install Django-Select2==5.4.0 \
    Fabric==1.10.2 \
    psycopg2 \
    Jinja2==2.8 \
    Markdown==2.6.5 \
    MarkupSafe==0.23 \
    MySQL-python==1.2.5 \
    Pillow==3.0.0 \
    PyYAML==3.11 \
    URLObject==2.4.0 \
    Unidecode==0.04.18 \
    argparse==1.2.1 \
    beautifulsoup4==4.4.1 \
    boto==2.38.0 \
    boto-rsync==0.8.1 \
    chardet==2.2.1 \
    django-ace==1.0.2 \
    django-ajax-selects==1.4.1 \
    django-appconf==1.0.1 \
    django-bower==5.0.4 \
    django-crispy-forms==1.5.2 \
    django-dajax==0.9.2 \
    django-dajaxice==0.7 \
    django-debug-toolbar==1.4 \
    django-extensions==1.5.9 \
    -e git+https://github.com/andreiavram/django_goodies@bbab26086046611debb867867c609df6143235e3#egg=django_goodies-master \
    django-imagekit==3.2.7 \
    django-less==0.7.2 \
    django-localflavor==1.2 \
    django-markdown==0.8.4 \
    django-model-utils==2.3.1 \
    django-pagedown==0.1.0 \
    django-pagination-bootstrap==1.0.7 \
    django-photologue==3.3.2 \
    django-qrcode==0.3 \
    django-recaptcha==1.0.4 \
    django-redis==4.3.0 \
    django-redis-cache==1.6.4 \
    django-sortedm2m==1.0.2 \
    django-storages==1.1.8 \
    django-taggit==0.17.5 \
    djangorestframework==3.3.1 \
    ecdsa==0.13 \
    gdata==2.0.18 \
    gunicorn==19.4.1 \
    hiredis==0.2.0 \
    longerusername==0.4 \
    markdown-checklist==0.4.1 \
    numpy==1.10.1 \
    oauthlib==1.0.3 \
    paramiko==1.16.0 \
    pilkit==1.1.13 \
    plasTeX==1.0 \
    pycrypto==2.6.1 \
    pyembed==1.3.1 \
    pyembed-markdown==1.1.0 \
    pyparsing==2.0.6 \
    python-memcached==1.57 \
    python-openid==2.2.5 \
    qrcode==5.1 \
    raven==5.8.1 \
    redis==2.10.5 \
    reportlab==3.2.0 \
    requests==2.8.1 \
    requests-oauthlib==0.5.0 \
    requests-toolbelt==0.5.0 \
    simplejson==3.8.1 \
    six==1.10.0 \
    sqlparse==0.1.18 \
    svglib==0.6.3 \
    svgwrite==1.1.6 \
    tablib==0.10.0 \
    wsgiref==0.1.2

#ADD . /scoutfile
#WORKDIR /scoutfile/web
#RUN mkdir /scoutfile/logs
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod a+x /wait-for-it.sh   

ADD ./deploy/requirements.txt /requirements.txt
#RUN pip install -r /scoutfile/deploy/requirements.txt
RUN pip install -r /requirements.txt

# CMD ["python", "./manage.py runserver 0.0.0.0:8000"]