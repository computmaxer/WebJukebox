## Django Google App Engine Skeletor

dj-gae-skeletor is a skeleton Django project handy for bootstrapping new
empty projects hosted with Google App Engine


### Features

Comes with:

  * [django-nonrel](https://bitbucket.org/wkornewald/django-nonrel/wiki/Home) - Non-relational backend support for Django via the new multi-db SQL compiler layer.
  * [djangoappengine](https://bitbucket.org/wkornewald/djangoappengine) - Django backends for App Engine support.
  * [djangotoolbox](https://bitbucket.org/wkornewald/djangotoolbox) - Small set of useful Django tools that are nonrel-compatible.
  * [django-autoload](https://bitbucket.org/twanschik/django-autoload) - Ensures loading of indexes or signal handlers before any request is being processed.
  * [django-dbindexer](https://bitbucket.org/wkornewald/django-dbindexer) - Adds support for SQL features like JOINs to non-relational Django backends


### Quick setup

Download [Google App Engine SDK](https://developers.google.com/appengine/downloads), unpack and add to PATH env variable.

    # create symbolic link to webob in project dir (in this case project dir is dj-gae-skeletor)
    ln -s <path_to_google_app_engine_sdk>/lib/<latest_webob>/webob webob

    # run
    python manage.py syncdb

    # run
    python manage.py runserver

    # manage.py remote allows you to execute a command on the production database
    # examples are:
    manage.py remote shell
    manage.py remote createsuperuser

  * Any app or module should be added to project dir
  * You can access datastore with: /_ah/admin/


### Deploying

If you haven't created application yet, go to [https://appengine.google.com/](https://appengine.google.com/) and create one.

Use created app name in app.yaml under application property.

    # run
    python manage.py deploy

You will have to login with google account.

In case of server errors go to [https://appengine.google.com/](https://appengine.google.com/), choose app and then Logs link in sidebar.
