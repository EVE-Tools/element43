Installation
============

This guide provides you with all the information you need to get your personal local development instance of element43 running, so you can start hacking on it as soon as possible. Should you encounter any problems do not hesitate to ask us on ``irc.coldfront.net`` on channel ``#element43``!

Prerequisites
-------------

Windows
^^^^^^^
You are running Windows? No problem! Get `VirtualBox <https://www.virtualbox.org>`_ and set up a Linux VM as element43 was not designed to run on Windows. It is recommended to pick a distribution like `Ubuntu Desktop <http://www.ubuntu.com/download/desktop>`_ for both running and editing element43. This gives you the advantage of having a self-contained portable development environment with all the editors and tools you need, instead of having to deal with transferring files between your host system and the guest system. Continue reading in the Linux section of this page once you are done installing Linux.

OS X
^^^^
Running element43 on OS X is simple. First, download and install Xcode 4 and its command line tools. Second, install the package manager `Homebrew <http://mxcl.github.com/homebrew/>`_ and run

    ``brew install libevent memcached libmemcached gfortran zeromq redis``

from your favorite terminal app. This installs the basic binary dependencies of element43. The only thing missing is the PostgreSQL server: Just download and install `Postgres.app <http://postgresapp.com>`_  The login credentials are:

    Host: ``localhost``

    User: ``<your os x user>``

    Password: ``<empty>``

You should change those parameters later on.
Finally, run

    ``sudo easy_install pip``

Linux
^^^^^
For running element43 on Linux you need several packages installed:

* ``libevent-dev``
* ``memcached``
* ``libmemcached-dev``
* ``gfortran``
* ``libzmq``
* ``postgresql-server``
* ``postgresql-client``
* ``python-dev``
* ``python-pip``

The actual names of the packages may vary in you distribution. You should be able to use this list with on Debian-based distros like Ubuntu. There are tons of tutorials on the net how to configure the individual components so this won't be covered in this article - just google around if you are not sure.

Setting up element43
--------------------

The following steps apply for all operating systems.

Setting up virtualenv
^^^^^^^^^^^^^^^^^^^^^
To keep all of element43's dependencies cleanly separated from your local packages, we will be setting up a virtualenv for the new installation.

* Create a new folder where you want to install element43 to
* ``cd`` into that folder and run ``sudo pip install virtualenv`` and ``sudo pip install virtualenvwrapper``
* Run ``source /usr/local/bin/virtualenvwrapper.sh`` and/or add this line to your ``.bashrc`` or ``.zshrc`` so you are able to use virtualenvwrapper without having to source it every single time
* Followed by ``mkvirtualenv element43`` to create a virtualenv named ``element43``

Forking / Cloning element43
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Unless you already have commit rights for the `main repository <https://github.com/EVE-Tools/element43>`_
, fork it into your own GitHub account so you can actually write to the repo.

* Run ``git clone <your repository url here>``

*From now on we will assume that your repo's root directory is called ``element43``.*

Installing Python dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Run ``add2virtualenv element43/webapp`` to add element43 to your Python path
* Run ``echo "export DJANGO_SETTINGS_MODULE=element43.settings.local" >> $VIRTUAL_ENV/bin/postactivate``
* Run ``echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate``
* Run ``export DJANGO_SETTINGS_MODULE=element43.settings.local``
* Run ``pip install numpy``
* Run ``pip install -r element43/requirements/local.txt`` to install the Python dependencies for developers

There is a high probability of this process failing (especially on Linux) mainly due to missing requirements. If you encounter any problems, have a close look at the error messages to identify the cause of the error. If cannot solve it on your own, head for the IRC.

Preparing the database
^^^^^^^^^^^^^^^^^^^^^^
* Create a database and a user called ``element43`` with the password ``element43`` using either the cli or a tool like `pgAdmin <http://www.pgadmin.org>`_ or `Navicat <http://www.navicat.com>`_
	* Ensure the new user has all rights for the newly-created database!
	* Only if you have no other choice edit the settings file at ``element43/webapp/element43/settings/local.py``
* Navigate to ``element43/webapp/`` then ``django-admin.py syncdb`` and **do not create a superuser**
* Run ``django-admin.py migrate eve_db``
* Run ``django-admin.py migrate apps.common``
* Run ``django-admin.py migrate apps.market_data``
* Run ``django-admin.py migrate apps.api``
* Run ``django-admin.py migrate djcelery``
* Download and extract the latest dump from `http://files.zweizeichen.org/dump.zip <http://files.zweizeichen.org/dump.zip>`_

* Import the dump with ``django-admin.py eve_import_ccp_dump <location of dump>``
* Seed your DB with the latest API info available from CCP via ``django-admin.py initapi``

Running element43
^^^^^^^^^^^^^^^^^
Ensure ``postgresql-server``, ``memcached`` and ``redis-server`` are running and properly configured

Gather initial market data
""""""""""""""""""""""""""
* Pick one of the two consumers available
    * Either the standard Python one located at ``element43/consumer/`` - its setup instructions are located on this site, too
    * Or the `100% hipster NodeJS one <https://github.com/EVE-Tools/node-43>`_ which is more efficient and does not require cron jobs to work properly, however you have to install NodeJS and npm first
* Let the consumer run for some hours to gather some initial data

Additional applications
"""""""""""""""""""""""
* Run ``django-admin.py celeryd -B -E`` for EVE API polling and several other scheduled tasks
* Run ``python pathfind.py`` at ``element43/pathfind`` for the pathfinding API

Running the devserver
"""""""""""""""""""""
* You should then be ready to run the development webserver (``element43/webapp``): ``django-admin.py runserver``
* Congratulations! You are ready to hack on element43 now :D

Further reading
^^^^^^^^^^^^^^^
Consider reading our :doc:`getting started guide <gettingstarted>`.
