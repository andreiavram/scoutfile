FROM django:1.8.7-python2

RUN apt-get update && apt-get install -y \
    git-core \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists

RUN pip install --upgrade pip
RUN pip install Django-Select2==5.4.0
RUN pip install Fabric==1.10.2
RUN pip install psycopg2
RUN pip install Jinja2==2.8
RUN pip install Markdown==2.6.5
RUN pip install MarkupSafe==0.23
RUN pip install MySQL-python==1.2.5
RUN pip install Pillow==3.0.0
RUN pip install PyYAML==3.11
RUN pip install URLObject==2.4.0
RUN pip install Unidecode==0.04.18
RUN pip install argparse==1.2.1
RUN pip install beautifulsoup4==4.4.1
RUN pip install boto==2.38.0
RUN pip install boto-rsync==0.8.1
RUN pip install chardet==2.2.1
RUN pip install django-ace==1.0.2
RUN pip install django-ajax-selects==1.4.1
RUN pip install django-appconf==1.0.1
RUN pip install django-bower==5.0.4
RUN pip install django-crispy-forms==1.5.2
RUN pip install django-dajax==0.9.2
RUN pip install django-dajaxice==0.7
RUN pip install django-debug-toolbar==1.4
RUN pip install django-extensions==1.5.9
RUN pip install -e git+https://github.com/andreiavram/django_goodies@bbab26086046611debb867867c609df6143235e3#egg=django_goodies-master
RUN pip install django-imagekit==3.2.7
RUN pip install django-less==0.7.2
RUN pip install django-localflavor==1.2
RUN pip install django-markdown==0.8.4
RUN pip install django-model-utils==2.3.1
RUN pip install django-pagedown==0.1.0
RUN pip install django-pagination-bootstrap==1.0.7
RUN pip install django-photologue==3.3.2
RUN pip install django-qrcode==0.3
RUN pip install django-recaptcha==1.0.4
RUN pip install django-redis==4.3.0
RUN pip install django-redis-cache==1.6.4
RUN pip install django-sortedm2m==1.0.2
RUN pip install django-storages==1.1.8
RUN pip install django-taggit==0.17.5
RUN pip install djangorestframework==3.3.1
RUN pip install ecdsa==0.13
RUN pip install gdata==2.0.18
RUN pip install gunicorn==19.4.1
RUN pip install hiredis==0.2.0
RUN pip install longerusername==0.4
RUN pip install markdown-checklist==0.4.1
RUN pip install numpy==1.10.1
RUN pip install oauthlib==1.0.3
RUN pip install paramiko==1.16.0
RUN pip install pilkit==1.1.13
RUN pip install plasTeX==1.0
RUN pip install pycrypto==2.6.1
RUN pip install pyembed==1.3.1
RUN pip install pyembed-markdown==1.1.0
RUN pip install pyparsing==2.0.6
RUN pip install python-memcached==1.57
RUN pip install python-openid==2.2.5
RUN pip install qrcode==5.1
RUN pip install raven==5.8.1
RUN pip install redis==2.10.5
RUN pip install reportlab==3.2.0
RUN pip install requests==2.8.1
RUN pip install requests-oauthlib==0.5.0
RUN pip install requests-toolbelt==0.5.0
RUN pip install simplejson==3.8.1
RUN pip install six==1.10.0
RUN pip install sqlparse==0.1.18
RUN pip install svglib==0.6.3
RUN pip install svgwrite==1.1.6
RUN pip install tablib==0.10.0
RUN pip install wsgiref==0.1.2

ADD . /scoutfile
WORKDIR /scoutfile
RUN mkdir web/logs

RUN pip install -r /scoutfile/deploy/requirements.txt

CMD ["python", "./manage.py runserver 0.0.0.0:8000"]