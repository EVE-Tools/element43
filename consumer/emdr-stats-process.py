#!/usr/bin/env python
"""
Rolls up the stats and shoves them into the database
Greg Oberfield gregoberfield@gmail.com
"""

import psycopg2
import ConfigParser
import os

# Turn on for standard output
TERM_OUT=False

def main():
        
    # Load connection params from the configuration file
    config = ConfigParser.ConfigParser()
    config.read('consumer.conf')
    dbhost = config.get('Database', 'dbhost')
    dbname = config.get('Database', 'dbname')
    dbuser = config.get('Database', 'dbuser')
    dbpass = config.get('Database', 'dbpass')
    redisdb = config.get('Redis', 'redishost')
    
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname)
    dbcon.autocommit = True

    curs = dbcon.cursor()
    
    sql = "INSERT INTO market_data_emdrstats (status_type, status_count, message_timestamp) SELECT status_type, count(id), now() FROM market_data_emdrstatsworking GROUP BY status_type"
    curs.execute(sql)
    
    sql = "TRUNCATE market_data_emdrstatsworking"
    curs.execute(sql)
    
if __name__ == '__main__':
    main()
