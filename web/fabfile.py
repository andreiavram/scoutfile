from fabric.api import env, prompt, get, local, run, hosts, cd
from fabric.contrib import django

django.project("scoutfile3")    # noqa
from django.conf import settings
from fabric.contrib import files
import os
import datetime

# this is needed here to evaluate settings here, and not in the fabric task
# workaround for this bug: https://github.com/fabric/fabric/issues/256
_ = settings.INSTALLED_APPS

@hosts('yeti.albascout.ro:24')
def seed_db():
    #   based on a script from http://www.iangeorge.net/articles/2010/jul/22/getting-live-data-mysqldump-and-fabric/
    data = (settings.DATABASES['default']['NAME'],
            settings.REMOTE_DB['host'],
            settings.REMOTE_DB['name'])

    env.hosts = [settings.REMOTE_DB["ssh_host"], ]
    env.user = settings.REMOTE_DB["ssh_user"]

    msg = prompt("Sure you want to get '%s' from '%s>%s'?" % data, default="y/n")

    if msg == "y":
        run('mysqldump --user %s --password=%s %s | gzip > /tmp/%s.sql.gz' % (
                settings.REMOTE_DB['user'],
                settings.REMOTE_DB['password'],
                settings.REMOTE_DB['name'],
                settings.REMOTE_DB['name']
                ))

        get('/tmp/%s.sql.gz' % settings.REMOTE_DB['name'], '/tmp/%s.sql.gz' % settings.DATABASES['default']['NAME'])
        local('gunzip < /tmp/%s.sql.gz | mysql -h %s -u %s -p\'%s\' -D %s' % (
                settings.DATABASES['default']['NAME'],
                settings.DATABASES['default']['HOST'],
                settings.DATABASES['default']['USER'],
                settings.DATABASES['default']['PASSWORD'],
                settings.DATABASES['default']['NAME']
                ), capture=False)


@hosts('yeti.albascout.ro:24')
def deploy_app():
    branch = os.environ['TRAVIS_BRANCH']
    branches_to_deploy = ["master", "develop"]

    if branch not in branches_to_deploy:
        print "Branch refused"
        return

    if not files.exists("~/releases"):
        run("mkdir ~/releases")

    if not files.exists("~/releases/{}".format(branch)):
        run("git clone git@github.com:andreiavram/scoutfile.git ~/releases/{}".format(branch))
        with cd("releases/{}/".format(branch)):
            run("git checkout {}".format(branch))
            run("virtualenv .venv")

    virtualenv_cmd = "source ~/releases/{}/.venv/bin/activate && ".format(branch)
    with cd("~/releases/{}".format(branch)):
        run("git checkout {}".format(branch))
        run("git pull")

        run(virtualenv_cmd + "pip install -r deploy/requirements.txt")

        folders_to_create = {"logs": "logs", "components": "components"}
        for folder, name in folders_to_create.items():
            if not files.exists(folder):
                run("mkdir {}".format(name))

        with cd("web/scoutfile3"):
            if not files.exists("local_settings.py"):
                run("ln -s ~/local_settings.{}.py local_settings.py".format(branch))

        if not files.exists("~/backup/{}/".format(branch)):
            run("mkdir -p ~/backup/{}".format(branch))

        with cd("web"):
            db_name = run(virtualenv_cmd + "./manage.py db_name")

        run("mysqldump -p$MYSQL_PASSWORD -u $MYSQL_USER {} > ~/backup/{}/{}.sql".format(
            db_name,
            branch,
            datetime.date.today().strftime("%d.%m.%Y")))

    with cd("~/releases/{}/web".format(branch)):
        run(virtualenv_cmd + "python manage.py bower install")
        run(virtualenv_cmd + "python manage.py collectstatic --noinput")
        run(virtualenv_cmd + "python manage.py migrate --noinput")

    run("sudo supervisorctl restart scoutfile-{}".format(branch))
