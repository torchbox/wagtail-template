#!/usr/bin/env python
import sys
import os
import shutil

from django.core.management import execute_from_command_line


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{{ project_name }}'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings.test")


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
