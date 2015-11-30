from fabric.api import run, env, cd
from django.conf import settings


def open_gate():
    with cd("/home/pi"):
        env.password = settings.GATEKEEPER_CONNECTION_PASSWORD
        run("sudo python releu.py")