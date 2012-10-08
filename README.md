element43
=========

Market, Trade and Industry Manager for EVE Online.

Initial Setup Instructions
------------------

Before you begin a word of warning: element43 was not designed to run in Windows!

* Make sure you have git installed.
* Make sure you have ``libevent`` and ``libmemcached`` installed.
  * OSX: ``brew install libevent`` and ``brew install libmemcached``
  * Debian: ``aptitude install libevent-dev libmemcached-dev``
* Create a virtualenv.
* ``pip install -r requirements.txt``
* Create a ``element43`` user and DB on Postgres.
* ``cd webapp`` then ``python manage.py syncdb`` and *do not create a superuser*
* Run ``python manage.py migrate eve_db``
* Run ``python manage.py migrate apps.market_data``
* Run ``python manage.py migrate apps.api``
* Run ``python manage.py migrate djcelery``
* Download and extract the latest dump from [https://github.com/gtaylor/django-eve-db/downloads](https://github.com/gtaylor/django-eve-db/downloads)
* Import the dump with ``python manage eve_import_ccp_dump <dump>``
* You should then be ready to run the development webserver: ``python manage.py runserver``
* Create a ``local_settings.py`` file and copy/paste/modify anything
  from ``settings.py`` that you'd like to change. This file won't be committed
  to git, and is safe to store passwords and dev workstation settings.

Applying DB schema migrations
-----------------------------

If you receive notice that an update requires a schema modification, you'll
want to run the following::

    python manage.py migrate
