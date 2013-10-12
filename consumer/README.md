EMDR-Consumer
=============

Python consumer for EMDR data feed

This requires redis-server, python-redis, hotqueue, zmq and pyzmq (with zmq.green extenstions).  Also requires EVE-Market-Data-Structures from Greg Taylor (https://github.com/gtaylor/EVE-Market-Data-Structures.git).

load-conquerable-stations.py should be run once a day to load new outposts.

warehouse-orders.py should generally be run via cron every 2-5 mins.

emdr-stats-process.py should run via cron every 5 mins.

Many thanks to Greg Taylor for assistance, example code and for creating EMDR.
