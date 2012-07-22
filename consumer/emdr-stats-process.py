#!/usr/bin/env python
"""
Rolls up the stats and shoves them into the database
Greg Oberfield gregoberfield@gmail.com
"""

import psycopg2

# Turn on for standard output
TERM_OUT=False

def main():
    dbcon = psycopg2.connect("host=192.168.1.41 user=element43 host=192.168.1.41 password=element43")
    dbcon.autocommit = True

    curs = dbcon.cursor()
    
    sql = "INSERT INTO market_data_emdrstats (status_type, status_count, message_timestamp) SELECT status_type, count(id), now() FROM market_data_emdrstatsworking GROUP BY status_type"
    curs.execute(sql)
    
    sql = "TRUNCATE market_data_emdrstatsworking"
    curs.execute(sql)
    
if __name__ == '__main__':
    main()
