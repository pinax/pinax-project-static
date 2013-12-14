pinax-project-static
====================

This purpose of this starter project is to provide a robust mocking and design
tool.


Usage:

    mkvirtualenv <project_name>
    pip install Django
    django-admin.py startproject --template=https://github.com/pinax/pinax-project-static/zipball/master <project_name>
    cd <project_name>
    ./manage.py syncdb --noinput
    ./manage.py runserver
