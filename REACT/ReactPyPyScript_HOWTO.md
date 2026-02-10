
# Classic Python project creation
- $ mkdir reactPyTest && cd reactPyTest
- $ python3 -m venv env
- source env/bin/activate
- (env) $ pip install django
- (env) django-admin startproject reactPyTest
- (env) cd reactPyTest
- 
- (env) django-admin startapp testPy
- (env) python3 manage.py migrate
- 
- (env) cd testPy
- (env) mkdir scripts
- (env) touch scripts/__init__.py

<u>scripts/load.py</u>

    from reactpy import component, html, run        #   <== reactpy import request

    @component
    def HelloWorld():
        return html.h1("Hello, World!")

    run(HelloWorld)
---
- (env) cd ..
- (env) pip install django_extensions
- (env) python3 manage.py check

<u>in PROJECTS/ReactPy/TESTS/reactPyTest/reactPyTest/reactPyTest/settings.py add to INSTALLED_APPS</u>

    - 'django_extensions',
    - 'testPy.apps.TestpyConfig',
---
    (env) python3 manage.py check
    (env) python3 manage.py makemigrations
    (env) python3 manage.py migrate

    (env) cd ~/PROJECTS/ReactPy/TESTS/reactPyTest/reactPyTest

# Reactpy installation inclusion
- s(env) pip install "reactpy[starlette]"
- s(env) python3 manage.py runscript load


