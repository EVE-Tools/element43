#!/usr/bin/env python
"""
Rolls up the stats and shoves them into the database
These stats are on a per-row basis for order messages, but only on a per message basis for history.
This is because we track inserts vs updates for orders.
Greg Oberfield gregoberfield@gmail.com
"""

import psycopg2
import ConfigParser
import os

def main():
        
    # Load connection params from the configuration file
    config = ConfigParser.ConfigParser()
    config.read('consumer.conf')
    dbhost = config.get('Database', 'dbhost')
    dbname = config.get('Database', 'dbname')
    dbuser = config.get('Database', 'dbuser')
    dbpass = config.get('Database', 'dbpass')
    dbport = config.get('Database', 'dbport')
    redisdb = config.get('Redis', 'redishost')
    TERM_OUT = config.get('Consumer', 'term_out')
    
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)
    dbcon.autocommit = True

    curs = dbcon.cursor()
    
    sql = "INSERT INTO market_data_emdrstats (status_type, status_count, message_timestamp) SELECT status_type, count(id), date_trunc('minute',now()) FROM market_data_emdrstatsworking GROUP BY status_type"
    curs.execute(sql)
    
    sql = "TRUNCATE market_data_emdrstatsworking"
    curs.execute(sql)
    
if __name__ == '__main__':
    main()
