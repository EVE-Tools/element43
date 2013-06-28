Getting started
===============

You want to join our effort of creating the ultimate community-driven EVE tool? Great!
It does not matter if you are coming from a .NET, PHP or Ruby background. Contributing to Element43 is easy and this guide will help you to get up and running, even if you do not know Python, HTML or CSS yet.

Python
^^^^^^
Element43's core web application is written in Python. If you already know a programming language, learning Python should not be a problem at all - you even might be able to skip this step and start learning Django directly. If you do not know any programming language, don't worry - it is an excellent language for beginners, too.

`learnpython.org <http://www.learnpython.org>`_ offers a nice interactive Python tutorial. After completing the basic section you will know enough Python to proceed with getting acquainted with Django.

Django
^^^^^^
Django is the web application framework element43 is built on and is similar to Ruby on Rails or CakePHP. Django has the same MVC (Model - View - Controller) or MTV (Model - Template - View) as many other web application frameworks (read more on this `here <http://www.djangobook.com/en/2.0/chapter05.html#the-mtv-or-mvc-development-pattern>`_). Together with the app structure this makes element43 modular and flexible enough to be the foundation of for example both a trade-finder and a corporate fitting manager.

Learning Django
"""""""""""""""
There are two very good sources for people who are new to Django. First, there is the official Django tutorial which walks you through creating your first Django app and teaches you the major concepts of the framework: `Django Tutorial <https://docs.djangoproject.com/en/1.5/intro/tutorial01/>`_
The second one is the free `Django Book <http://www.djangobook.com/>`_. Some parts could be slightly out of date, however it still is a intelligible reference for most basic topics. For more in-depth and elaborate explanations there is `Django's excellent documentation <https://docs.djangoproject.com>`_. Getting into Django can be difficult at times. Don't be afraid of asking questions in our IRC.

For more advanced developers we recommend getting `Two Scoops of Django <https://django.2scoops.org>`_ which contains various best-practices for Django projects we are following in element43.

Installing element43 on your dev box
""""""""""""""""""""""""""""""""""""
:doc:`Installation <installation>` is covered in its own document. You'll want perform a local installation instead of deploying it on let's say your VPS. This makes it far more easy to quickly evaluate code changes. Also take your time and click through the project so that you get a basic understanding of element43's structure.


Models
""""""
Element43 is all about data. It's no wonder that the models play a very important role in the project. Luckily we already have done most of the work for you, like mapping CCPs entire static data dump to the appropiate models or collecting all kinds of market data. This allows you to conveniently access all this data via Django's ORM so you can do stuff like this:

.. highlight:: python

::

    # Necessary Model imports
    from eve_db.models import MapSolarSystem
    from apps.market_data.models import Orders

    #
    # Getting the entire market of Jita
    #

    # 1. Get the solar system named Jita
    jita = MapSolarSystem.objects.get(name='Jita')

    # 3. Get all orders in Jita
    market_jita = Orders.active.filter(mapsolarsystem=jita)

    # Of course you could also do
    market_jita_by_id = Orders.active.filter(mapsolarsystem=30000142)

    #
    # Some ORM magic
    #

    # Printing Jita's region's name (The Forge)
    print(jita.region.name)

Django's interactive shell which you can access via ``django-admin.py shell`` provides a handy playground for experimenting with queries.

As you can see there is no raw SQL involved and relations can be traversed with ease. Note the difference between selecting Orders and a regular model. While we call ``.objects`` on regular objects, we have added ``.active`` for selecting active orders to save you from always having to filter for ``is_active`` when searching through the market.

For documentation on CCP's SDE have a look at `eve-id.net <http://wiki.eve-id.net/Category:CCP_DB_Tables>`_. The ORM mapping and import is handled via `django-eve-db <https://github.com/gtaylor/django-eve-db>`_ - the code of the models should be self-explanatory.

Market data is handled by the models of the app ``market_data``- documentation can be found in the :doc:`applications document<apps>`.
Again - if you have problems, ask for help in IRC.

Templates
"""""""""
Element43's templates are written in HamlPy instead of Dajngo-flavoured HTML. This has various reasons - the main one is that it saves you a ton of code. To get into front-end development it's recommended to learn basic HTML and CSS first. 'Learning' HAML will be a piece of cake then, since it's only an abstraction of HTML.

A nice introduction into HTML and CSS can be found at `Shay Howe's <http://learn.shayhowe.com/html-css/>`_ website. To learn HAML, have a look at the templates and the `reference <http://haml.info/docs/yardoc/file.REFERENCE.html>`_ - our sytax is slightly different, since we are using HamlPy which docs can be found `on GitHub <https://github.com/jessemiller/HamlPy>`_.

Furthermore element43 uses a customzied version of Twitter's Bootstrap (Bootswatch Cyborg theme + custom SCSS) for the easy creation of layouts and UI elements like buttons or tables: `Documentation <http://twitter.github.com/bootstrap/>`_


Writing your first app
^^^^^^^^^^^^^^^^^^^^^^
Django allows us to create independent modules called ``apps``. An app often serves a single purpose like tradefinding or the management of API update tasks. Each app not only can have its own models, views, tasks and templates, but can also re-use common functions or models from other apps.
First, you'll want to fork our repository at GitHub, so you have a nice versioned base for your new module. Getting your first app up and running is simple. We'll create an app called ``myapp`` which will serve some static content fetched from the DB.

1. Create a folder named ``myapp``inside the ``apps`` directory
2. In that newly created folder create 3 empty files:
  - ``__init__.py`` - So Python knows that your app is a module
  - ``urls.py``- The file containing your URL patterns
  - ``views.py``- The file containing your views
3. Create a folder named ``templates`` in ``myapp``

Now you have to tell Django where to find your app. Just add ``apps.myapp`` to the ``INSTALLED_APPS`` tuple in ``settings/base.py`` (don't forget the comma).
That's basically it. Let's add some functionality now:

``apps/myapp/urls.py``

.. highlight:: python

::

    # Necessary URL imports
    from django.conf.urls import patterns, url

    # The URL patterns for your app
    urlpatterns = patterns('apps.myapp.views',
        # History JSON
        url(r'^start/$', 'start', name='myapp_start'),
    )

Here we've created an url pattern called ``myapp_start`` that calls the function ``start`` inside your ``views.py`` whenever ``start/`` is matched. In order for that route to work, we have to add the new app's url patterns to the global URL list at ``/urls.py``:

``apps/myapp/urls.py``

.. highlight:: python

::

    [...]

    #
    # URLs for Element43
    #

    urlpatterns = patterns('',

        [...]
        # Add myapp's URLs to /myapp
        url(r'^myapp/, include('apps.myapp.urls')),
        [...]
    )

This will mount myapp's URLs under ``[root]/myapp``. Now that your routes have been added to the main application's router - we can add a view and a template.

``apps/myapp/views.py``

.. highlight:: python

::
    # Imports
    from django.shortcuts import render_to_response
    from django.template import RequestContext

    # Models
    from eve_db.models import MapSolarSystem


    def start(request):

        """
        Returns information about Jita
        """

        # Get the object from DB
        jita = MapSolarSystem.objects.get(name='Jita')

        # Add that object to our context, so we can use it in our template
        rcontext = RequestContext(request, {'system_object': jita})

        # Render our template
        return render_to_response('myapp_start.haml', rcontext)

Create a file called ``myapp_start.haml`` inside ``apps/myapp/templates``.

``apps/myapp/templates/myapp_start.haml``

::

    - extends "base.haml"
    - block title
      = block.super
      This is my new app's title :D
    - block content
      %h1
        = system_object.name
      %p
        Region: {{system_object.region.name}}

Once you have done all that, run ``django-admin.py runserver``, open ``http://localhost:8000/myapp/start/`` and admire your first app.
I recommend you to play around with all kinds of models, parameters in the URL (just look at the existing apps to see how that works) and the layout - especially Bootstrap's built-in classes. Try to change small things at first and then work your way up to the bigger ones - that way you'll quickly learn how to do stuff with Element43.

Once you're done with creating something useful, just send us a pull request and we'll review your code then and merge it into the main repository.

Miscellaneous
^^^^^^^^^^^^^

Coding Style
""""""""""""
We like to stick with the `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_ coding style guidelines with certain exceptions like a character limit of 120 characters per line. Please also comment you code extensively and use docstrings whenever possible!

Git
"""
Element43's repository is stored at GitHub - to familiarize yourself with git we recommend taking the free `TryGit <http://try.github.com/levels/1/challenges/1>`_ course.

Code Editor
"""""""""""
The team uses all kinds of editors and IDEs including:

* `Sublime Text <http://www.sublimetext.com>`_ - Cross-platform extensible editor
    * Try the sublime package manager and install ``SublimeLinter``, ``Hamlpy``, ``Python PEP8 Autoformat``, ``SublimeCodeIntel``, ``SublimeLinter`` and ``SublimeRope`` - those are some really useful packages which add IDE-like features without slowing-down the editor
* `Komodo IDE <http://www.activestate.com/komodo-ide>`_ - Cross-platform IDE
* `Chocolat <http://chocolatapp.com>`_ - Pretty Mac OS only IDE