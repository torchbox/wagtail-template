{% if False %}

Wagtail template
================

THIS PROJECT IS NO LONGER MAINTAINED

Use the new ``wagtail-cookiecutter`` repo instead: https://github.com/torchbox/wagtail-cookiecutter

Setup
-----

Make sure that you have Django installed on your machine.

To start a new project, run the following commands::

    django-admin.py startproject shortname --template=https://github.com/torchbox/wagtail-template/zipball/master --name=Vagrantfile,Dockerfile --ext=html,rst,md,pp,ini
    cd shortnamewagtail
    vagrant up
    vagrant ssh -- -A
      (then, within the SSH session:)
    dj createsuperuser
    djrun

Where 'shortname' is the acronym for your project. So London Sport would be 'ls'.

This will make the app accessible on the host machine as http://localhost:8000/ . The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

For more extensive instructions see https://wiki.torchbox.com/view/Setting_up_a_Wagtail_Server

{% endif %}

{{ project_name }}
==================
