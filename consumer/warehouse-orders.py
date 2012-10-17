#!/usr/bin/env python

"""
Go through the seenOrders table, find all NOT IN that set for each region/type combo and delete
Greg Oberfield - gregoberfield@gmail.com
"""

import psycopg2
import psycopg2.extras
import time
import ConfigParser
import os
import re
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
from hotqueue import HotQueue
import sys

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read(['consumer.conf', 'local_consumer.conf'])
dbhost = config.get('Database', 'dbhost')
dbname = config.get('Database', 'dbname')
dbuser = config.get('Database', 'dbuser')
dbpass = config.get('Database', 'dbpass')
dbport = config.get('Database', 'dbport')
redisdb = config.get('Redis', 'redishost')
TERM_OUT = config.get('Consumer', 'term_out')

# Connect to PostgreSQL, auto commit.
# Handle DBs without password
if not dbpass:
    # Connect without password
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" dbname="+dbname+" port="+dbport)
else:
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)
dbcon.autocommit = True

# Connect to PostgreSQL, no auto commit
# Handle DBs without password
if not dbpass:
    # Connect without password
    transdbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" dbname="+dbname+" port="+dbport)
else:
    transdbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)

# Activate all cursors
curs = dbcon.cursor()
#sscurs = transdbcon.cursor('loopcurs', cursor_factory=psycopg2.extras.DictCursor)

# Fire up the regex cannon
recannon = re.compile("\((\d+),(\d+)\)")

workers = []
combo = {}
    
def main():

    curs = dbcon.cursor()
    
    # create and copy the data over
    sql = "CREATE TABLE IF NOT EXISTS market_data_seenordersworking (LIKE market_data_seenorders)"
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print e.pgerror
        sys.exit(1)
    sql = "TRUNCATE market_data_seenordersworking"
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print e.pgerror
        sys.exit(1)
    sql = "INSERT INTO market_data_seenordersworking SELECT * FROM market_data_seenorders"
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print e.pgerror
        sys.exit(1)
    sql = "TRUNCATE market_data_seenorders"
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print e.pgerror
        sys.exit(1)
    
    sql = "SELECT DISTINCT region_id FROM market_data_seenordersworking"
    curs.execute(sql)
    for result in curs:
        workers.append(gevent.spawn(thread, result[0]))
    
    gevent.joinall(workers)
    
def thread(region):
    
    tcurs = dbcon.cursor()
    sql = "SELECT DISTINCT type_id FROM market_data_seenordersworking WHERE region_id=%s" % int(region)
    tcurs.execute(sql)
    result = tcurs.fetchall()
    if result == None:
        if TERM_OUT==True:
            print "No Results"
    else:
        for row in result:
            if TERM_OUT==True:
                print "Region: ", region, "Type: ", row[0]
            #rowdata = recannon.match(row[0])
            typeID = row[0]
            sql = """UPDATE market_data_orders SET is_active = 'f'
                        WHERE mapregion_id=%s AND invtype_id=%s AND is_active='t' AND market_data_orders.id
                        NOT IN (SELECT id FROM market_data_seenordersworking WHERE mapregion_id=%s AND invtype_id=%s)""" % (region, typeID, region, typeID)
            try:
                tcurs.execute(sql)
            except psycopg2.DatabaseError, e:
                print e.pgerror
                pass
            if TERM_OUT==True:
                print "Type: ", typeID, " Region: ", region, " (affected: ", tcurs.rowcount, ")"
            sql = "DELETE FROM market_data_seenordersworking WHERE region_id=%s AND type_id=%s" % (region, typeID)
            try:
                tcurs.execute(sql)
            except psycopg2.DatabaseError, e:
                print e.pgerror
                pass
    
if __name__ == '__main__':
    main()
