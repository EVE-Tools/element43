Consumer Documentation
======================

  REQUIREMENTS
  
  The consumer works off of the Eve-Market-Data-Relay feed.  This requires a number of modules (see requirements.txt) to be installed.  Additionally, you will need to have Zer0MQ installed (https://github.com/zeromq/zeromq2-x.git) and the pyzmq module installed from source (https://github.com/zeromq/pyzmq.git).  See their respective documentation for how to install.

  INSTALLATION

  See the consumer.conf file - you can override any settings by creating a "local_consumer.conf" file and use the same sections/variable names (anything in local will override consumer.conf).  It is not recommended to change consumer.conf since that will get overwritten every time you pull from the repo.

