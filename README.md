element43
=========

Market, Trade and Industry Manager for EVE Online. Element43 aims to provide players of the MMORPG EVE Online with an
all-in-one experience for managing their in-game enterprises. The application can be extended via Django's apps in a
modular way, so that developers can easily put the massive amount of data collected by Element43 to use without conflicting
with each other.

Initial Setup
-------------

Detailed instructions for multiple platforms can be found here: [https://element43.readthedocs.org/en/latest/installation.html](https://element43.readthedocs.org/en/latest/installation.html)

Documentation
-------------

Documentation for developers is located at [ReadTheDocs](https://element43.readthedocs.org/en/latest/).

Applying DB schema migrations
-----------------------------

There is one index that needs to be built manually due to limitations in South.  You will want to build an index in the market_data_orders table similar to:

``"market_data_orders_mia" btree (mapregion_id, invtype_id, is_active) WHERE is_active = true``

Yes that is for postgresql, not quite sure what the equivalent is for MySQL.

Without this database performance will be atrocious to the point of killing your site.

If you receive notice that an update requires a schema modification, you'll
want to run the following::

    python manage.py migrate
