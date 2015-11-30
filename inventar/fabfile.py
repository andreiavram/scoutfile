from fabric.api import run, env, cd


def open_gate():
    with cd("/home/pi"):
        run("sudo python releu.py")