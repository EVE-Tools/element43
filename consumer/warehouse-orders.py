#!/usr/bin/env python

"""
Go through the seenOrders table, find all NOT IN that set for each region/type combo and delete
Greg Oberfield - gregoberfield@gmail.com
"""

import MySQLdb as mdb
import time

# Turn on for standard output
TERM_OUT=False

dbhost="localhost"
dbname = "dbname"
dbuser = "dbuser"
dbpass = "dbpass"

def main():
    dbcon = mdb.connect(dbhost, dbuser, dbpass, dbname)
    curs = dbcon.cursor()
    
    # create and copy the data over
    sql = "DROP TABLE IF EXISTS seenOrdersWorking"
    curs.execute(sql)
    sql = "CREATE TABLE seenOrdersWorking LIKE seenOrders"
    curs.execute(sql)
    sql = "INSERT INTO seenOrdersWorking SELECT * FROM seenOrders"
    curs.execute(sql)
    sql = "TRUNCATE seenOrders"
    curs.execute(sql)
    loopsql = "SELECT * FROM seenOrdersWorking ORDER BY typeID, regionID LIMIT 1"
    while (curs.execute(loopsql)):
        row = curs.fetchone()
        regionID = row[2]
        typeID = row[1]
        sql = """INSERT IGNORE INTO marketDataWarehouse (generatedAt, regionID, typeID, price, `range`, orderID, bid, issueDate, duration, volumeEntered, stationID, solarSystemID, ipHash, suspicious) 
                 SELECT generatedAt, regionID, typeID, price, `range`, orderID, bid, issueDate, duration, volumeEntered, stationID, solarSystemID, ipHash, suspicious FROM marketData
                 WHERE typeID=%s AND regionID=%s AND marketData.orderID NOT IN (SELECT orderID FROM seenOrdersWorking WHERE typeID=%s AND regionID=%s)""" % (typeID, regionID, typeID, regionID)
        curs.execute(sql)
        sql = "DELETE FROM marketData WHERE typeID=%s AND regionID=%s AND marketData.orderID NOT IN (SELECT orderID FROM seenOrdersWorking WHERE typeID=%s AND regionID=%s)" % (typeID, regionID, typeID, regionID)
        curs.execute(sql)
        if TERM_OUT==True:
            print "Type: ", typeID, " Region: ", regionID, " (affected: ", curs.rowcount, ")"
        sql = "DELETE FROM seenOrdersWorking WHERE typeID=%s AND regionID=%s" % (typeID, regionID)
        curs.execute(sql)
        dbcon.commit()
    
if __name__ == '__main__':
    main()
