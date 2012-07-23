#!/usr/bin/env python
"""
Get the data from EMDR and shove it into the redis queue
Greg Oberfield gregoberfield@gmail.com
"""

import zlib
import zmq.green as zmq
import gevent
import ConfigParser
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
from hotqueue import HotQueue

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read('consumer.conf')
redisdb = config.get('Redis', 'redishost')
relay = config.get('EMDR', 'relay')


# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 200

queue =  HotQueue("emdr-messages", host=redisdb, port=6379, db=0)

def main():
    """
    main flow of the app
    """
    
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    
    # connect to the first publicly available relay
    subscriber.connect(relay)
    # disable filtering
    subscriber.setsockopt(zmq.SUBSCRIBE, "")
    
    print("Connected to %s" % relay)
    
    # use a greenlet pool to cap the number of workers at a reasonable level
    greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)
    
    print("Consumer daemon started, waiting for jobs...")
    print("Worker pool size: %d" % greenlet_pool.size)
    
    while True:
        # since subscriber.recv blocks when no messages are available
        # this loop stays under control.  if something is available and the
        # greenlet pool has greenlets available for use, work gets done
        greenlet_pool.spawn(worker, subscriber.recv())
        
def worker(job_json):
    """
    For every incoming message, this worker function is called.  Be extremely
    careful not to do anything cpu intensive here, or you will see blocking.
    Sockets are async under gevent, so those are fair game
    """

    # Push the message onto the queue
    queue.put(job_json)
    
        

if __name__ == '__main__':
    main()

