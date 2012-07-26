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

def main():
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
    mcserver = config.get('Memcache', 'server')
    mckey = config.get('Memcache', 'key')
    
    # Connect to PostgreSQL, auto commit.
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)
    dbcon.autocommit = True

    # Connect to PostgreSQL, no auto commit
    transdbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)

    # Activate all cursors
    curs = dbcon.cursor()
    sscurs = transdbcon.cursor('loopcurs', cursor_factory=psycopg2.extras.DictCursor)

    # Fire up the regex cannon
    recannon = re.compile("\((\d+),(\d+)\)")

    # create and copy the data over
    sql = "DROP TABLE IF EXISTS market_data_seenordersworking"
    curs.execute(sql)
    sql = "CREATE TABLE market_data_seenordersworking (LIKE market_data_seenorders)"
    curs.execute(sql)
    sql = "INSERT INTO market_data_seenordersworking SELECT * FROM market_data_seenorders"
    curs.execute(sql)
    sql = "TRUNCATE market_data_seenorders"
    curs.execute(sql)
    """
    loopsql = "SELECT * FROM market_data_seenordersworking ORDER BY type_id, region_id LIMIT 1"
    execute = True
    while (execute):
        try:
            curs.execute(loopsql)
        except psycopg2.DatabaseError, e:
            pass
        row = curs.fetchone()
        if row:
            regionID = row[1]
            typeID = row[2]
            sql = INSERT INTO market_data_orderswarehouse (generated_at, region_id, type_id, price, order_range, id, is_bid, issue_date, duration, volume_entered, station_id, solar_system_id, uploader_ip_hash, message_key, is_suspicious) 
                     SELECT generated_at, region_id, type_id, price, order_range, id, is_bid, issue_date, duration, volume_entered, station_id, solar_system_id, uploader_ip_hash, message_key, is_suspicious FROM market_data_orders
                     WHERE type_id=%s AND region_id=%s AND market_data_orders.id NOT IN (SELECT id FROM market_data_seenordersworking WHERE type_id=%s AND region_id=%s) % (typeID, regionID, typeID, regionID)
            try:
                curs.execute(sql)
            except psycopg2.DatabaseError, e:
                pass
            sql = "DELETE FROM market_data_orders WHERE type_id=%s AND region_id=%s AND market_data_orders.id NOT IN (SELECT id FROM market_data_seenordersworking WHERE type_id=%s AND region_id=%s)" % (typeID, regionID, typeID, regionID)
            try:
                curs.execute(sql)
            except psycopg2.DatabaseError, e:
                pass
            if TERM_OUT==True:
                print "Type: ", typeID, " Region: ", regionID, " (affected: ", curs.rowcount, ")"
            sql = "DELETE FROM market_data_seenordersworking WHERE type_id=%s AND region_id=%s" % (typeID, regionID)
            try:
                curs.execute(sql)
            except psycopg2.DatabaseError, e:
                pass
        else:
            execute = False
    """
    
    sscurs.execute("SELECT distinct(region_id, type_id) FROM market_data_seenordersworking")
    for row in sscurs:
        rowdata = recannon.match(row[0])
        regionID = rowdata.group(1)
        typeID = rowdata.group(2)
        sql = """INSERT INTO market_data_orderswarehouse (generated_at, region_id, type_id, price, order_range, id, is_bid, issue_date, duration, volume_entered, station_id, solar_system_id, uploader_ip_hash, message_key, is_suspicious) 
                 SELECT generated_at, region_id, type_id, price, order_range, id, is_bid, issue_date, duration, volume_entered, station_id, solar_system_id, uploader_ip_hash, message_key, is_suspicious FROM market_data_orders
                 WHERE type_id=%s AND region_id=%s AND market_data_orders.id NOT IN (SELECT id FROM market_data_seenordersworking WHERE type_id=%s AND region_id=%s)""" % (typeID, regionID, typeID, regionID)
        try:
            curs.execute(sql)
        except psycopg2.DatabaseError, e:
            pass
        sql = "DELETE FROM market_data_orders WHERE type_id=%s AND region_id=%s AND market_data_orders.id NOT IN (SELECT id FROM market_data_seenordersworking WHERE type_id=%s AND region_id=%s)" % (typeID, regionID, typeID, regionID)
        try:
            curs.execute(sql)
        except psycopg2.DatabaseError, e:
            pass
        if TERM_OUT==True:
            print "Type: ", typeID, " Region: ", regionID, " (affected: ", curs.rowcount, ")"
        sql = "DELETE FROM market_data_seenordersworking WHERE type_id=%s AND region_id=%s" % (typeID, regionID)
        try:
            curs.execute(sql)
        except psycopg2.DatabaseError, e:
            pass
    
    
if __name__ == '__main__':
    main()
