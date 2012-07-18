#!/usr/bin/env python
"""
Rolls up the stats and shoves them into the database
Greg Oberfield gregoberfield@gmail.com
"""

import MySQLdb as mdb

# Turn on for standard output
TERM_OUT=False

dbhost="localhost"
dbname = "dbname"
dbuser = "dbuser"
dbpass = "dbpass"

def main():
    dbcon = mdb.connect(dbhost, dbuser, dbpass, dbname)
    curs = dbcon.cursor()
    
    sql = "INSERT INTO emdrStats (statusType, statusCount) SELECT statusType, count(id) FROM emdrStatsWorking GROUP BY statusType"
    curs.execute(sql)
    
    sql = "TRUNCATE emdrStatsWorking"
    curs.execute(sql)
    
    dbcon.commit()
    
if __name__ == '__main__':
    main()
