from fabric.api import env, prompt, get, local, run, hosts
from fabric.contrib import django

django.project("scoutfile3")    # noqa
from django.conf import settings


@hosts('yeti.albascout.ro:24')
def seed_db():
    #   based on a script from http://www.iangeorge.net/articles/2010/jul/22/getting-live-data-mysqldump-and-fabric/
    data = (settings.DATABASES['default']['NAME'],
            settings.REMOTE_DB['host'],
            settings.REMOTE_DB['name'])

    env.hosts = ["lair", ]
    env.user = "yeti"

    msg = prompt("Sure you want to get '%s' from '%s>%s'?" % data, default="y/n")

    if msg == "y":
        run('mysqldump --user %s --password=%s %s | gzip > /tmp/%s.sql.gz' % (
                settings.REMOTE_DB['user'],
                settings.REMOTE_DB['password'],
                settings.REMOTE_DB['name'],
                settings.REMOTE_DB['name']
                ))

        get('/tmp/%s.sql.gz' % settings.REMOTE_DB['name'], '/tmp/%s.sql.gz' % settings.DATABASES['default']['NAME'])
        local('gunzip < /tmp/%s.sql.gz | mysql -u %s -p%s -D %s' % (
                settings.DATABASES['default']['NAME'],
                settings.DATABASES['default']['USER'],
                settings.DATABASES['default']['PASSWORD'],
                settings.DATABASES['default']['NAME']
                ), capture=False)
