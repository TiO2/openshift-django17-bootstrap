Python 3 + Django 1.7 + PostgreSQL with Openshift
===================================================


This repository is an enabler to run Django (1.7) applications with Python 3.x on [OpenShift](https://openshift.redhat.com/). It is modified from (https://github.com/lrivallain/openshift-django1.7-py3).

It has been tested for Python 3.3, 3.4 but it should also work for Python 2. 

Prerequisites
-------------

You need to have an OpenShift account: if not, [create a new one](https://www.openshift.com/app/account/new).

Secondly, you need to install and configure `rhc` tools on your computer:

    gem install rhc
    rhc setup

Thirdly, you need to create a new OpenShift application with Python 3.x cartridge: 
- By web interface: [new python 3.3 app](https://openshift.redhat.com/app/console/application_type/cart!python-3.3) + git clone
- By command line: `rhc app create -a mynewapp -t python-3.3`

Notice your git remote address for later use.

Add django enabler
------------------

Add this upstream repo:

    $ mkdir mysite
    $ cd mysite
    $ git init
    $ git remote add upstream -m master git@github.com:TiO2/openshift-django17-bootstrap.git
    $ git pull -s recursive -X theirs upstream master

Configuration
-------------

Django "secret key" is already set for localhost usage. For production/OpenShift cartridge, you'll have to set a new secret one.

### Generate a new secret key

Django "secret key" is already set for localhost usage. For production/OpenShift cartridge, you'll have to set a new secret one.

You can use a web service like: [Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)
Or by using python command line:  

    import random
    print(''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for n in range(60)]))

### Push key to the cartridge

When key is generated, you need to set an environment variables on the OpenShift cartridge:

    rhc set-env DJANGO_SETTINGS_SECRET_KEY="your-secret-key" -a mynewapp

### Database backend

In `wsgi/openshift/settings.py`, POSTGRESQL backend is configured. If you whant to use one, you'll need to have a database cartridge to your app. Examples:

MySQL:

    rhc cartridge add mynewapp mysql-5.5
    rhc cartridge add mynewapp phpmyadmin-4

PostgreSQL:

    rhc cartridge add mynewapp postgresql-9.2

...

Then you may have to adapt settings according to your database backend (with the help of OpenShift ['Using Environment Variables' documentation](https://developers.openshift.com/en/managing-environment-variables.html)):

```
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
if ON_OPENSHIFT: # production settings
    DATABASES = {
         'default': { # you can change the backend to any django supported
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     os.environ['OPENSHIFT_APP_NAME'],
            'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
         }
    }
...
```

### First push

After local changes, 

    $ git add .
    $ git commit -m "commit comment"

    $ git remote add openshift -f *the git remote address for your app*
    $ git merge openshift/master -s recursive -X ours 
    $ git push openshift HEAD


Django super user
-----------------
After first push, your application do not have a super user (admin). You have to create one:

    rhc ssh mynewapp
    source $OPENSHIFT_HOMEDIR/python/virtenv/venv/bin/activate
    python "$OPENSHIFT_REPO_DIR"wsgi/manage.py createsuperuser
    
    
### Create a local development environment

We need to create a local environment for develop and test our application before upload it to OpenShift.

A python virtaulenv is recommended. 

Create a virtualenv and activate it:

    $ cd mysite
    $ virtualenv venv --no-site-packages
    $ source venv/bin/activate


Install dependencies: 

    $ python setup.py install

Testing the install.

In the wsgi/openshift directory, execute:

    $ python manage.py runserver
    



    
