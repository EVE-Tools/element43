Architecture
============

At first element43's structure might seem a little intimidating to someone who is new to Django or similar frameworks. This document is for understanding the app's basic structure. Each part has or will have its own, detailed documentation. Element43 is basically made up of three parts: the consumer the webapp and the pathfinding API.

Consumer
^^^^^^^^
The consumer connects to `EMDR's <https://eve-market-data-relay.readthedocs.org/en/latest/>`_ data feed and stores market data into the tables prefixed with ``market_data_``. The consumer also analyzes incoming data for suspicious orders and does some basic statistical processing to speed-up the main application. Currently there are two consumers available:

* A python based one located at ``element43/consumer``
    * Documentation can be found here, too
* And `a NodeJS based one <https://github.com/EVE-Tools/node-43>`_ which aims to be more efficient

Django Web App
^^^^^^^^^^^^^^
This is the main part of element43. It handles all the functionality of displaying data, importing data from CCP's API and authentication of users. In order to keep things clear and modular, element43 is divided into several apps of which each one is only performing a very specific set of tasks. This way every app has access to all the data stored in the database and some common functions without the code getting confusing.

Currently there are eight different apps in ``element43/webapp/element43/apps/``:

+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
|      App      |                                                                                        Function                                                                                         |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| api           | Handles EVE API imports and associated models. Does not actually render anything. Mainly contains Celery tasks and API models.                                                          |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| auth          | Handles the registration, authentication and deactivation of expired accounts. Does not contain any models.                                                                             |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| common        | Renders all the basic templates like ``home`` and ``about``. Also contains ``util.py`` with many useful shared functions.                                                               |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| dashboard     | App for displaying the dashboard and character information once the user logged in.                                                                                                     |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| manufacturing | An advanced manufacturing calculator.                                                                                                                                                   |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| market_data   | Element43's largest app. This app contains the models for market data as well as the related views such as quicklook, regional quicklook, station ranking and station and import views. |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| user_settings | Presents the user account settings. Allows for adding API keys, characters or changing profile information.                                                                             |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+
| wallet        | Displays wallet-specific information like the journal or transactions using the API models.                                                                                             |  |
+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--+


*See the model and database documentation for further information*

Pathfinding
^^^^^^^^^^^
The pathfinding app provides a basic HTTP-based pathfinding API.