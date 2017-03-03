#!/usr/bin/env python
import os
import sys
# import pydevd
# pydevd.settrace('192.168.33.1', port=8001, stdoutToServer=True, stderrToServer=True)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scoutfile3.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
