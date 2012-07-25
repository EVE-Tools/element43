Consumer Documentation
======================

Description
-----------

The consumer consists of five scripts:

* *emdr-enqueue.py*
  This script connects to the remote relay(s) and grabs incoming messages and shoves them onto the "emdr-messages" queue in redis, making them available
  to the dequeue script.
* *emdr-dequeue.py*
  This is the main workhorse.  We generally run from 2-4 of these processes at once as it's "threaded" with greenlets.  Really 1 is sufficient to keep up with
  message frequency but redundancy isn't a bad thing and redis makes sure the processes don't get duplicate messages.  This script does all the processing of incoming
  EMDR messages - validating and inserting them into the database.
* *emdr-stats-process.py*
  This script runs every 5 minutes from cron.  It rolls up the current messages processed and puts them into the tracker table for us to output statistics.
* *warehouse_orders.py*
  This script runs every 2 minutes from cron.  It goes through and looks at all orders processed in the last 2 minutes and moves orders not seen in a region/type combo
  to the "warehouse" table -- ie, they are completed (either cancelled, purchased/sold, etc -- no longer available).
* *load_conquerable_stations.py*
  This script runs once a day (we run it during downtime).  It goes and loads all the user-built outposts and puts them into the staStations table in the static data dump
  so that they will display properly when pulling up orders.

Requirements
------------
  
The consumer works off of the Eve-Market-Data-Relay feed.  This requires a number of modules (see requirements.txt) to be installed.
Additionally, you will need to have Zer0MQ installed (https://github.com/zeromq/zeromq2-x.git) and the pyzmq module installed from source (https://github.com/zeromq/pyzmq.git).
See their respective documentation for how to install.

Also required:

* redis

Optional, but useful:

* hotwatch

Installation
------------

See the consumer.conf file - you can override any settings by creating a "local_consumer.conf" file and use the same sections/variable names (anything in local will override consumer.conf).
It is not recommended to change consumer.conf since that will get overwritten every time you pull from the repo.

