#!/usr/bin/env python
"""
Get the conquerable station list from the API and load it into the SDD database
Greg Oberfield gregoberfield@gmail.com
"""

import psycopg2
import urllib
from xml.dom import minidom

TERM_OUT = True

dbhost="localhost"
dbname = "dbname"
dbuser = "dbuser"
dbpass = "dbpass"

def main():
    dbcon = mdb.connect(dbhost, dbuser, dbpass, dbname)
    curs = dbcon.cursor()

    apiURL = 'https://api.eveonline.com/eve/ConquerableStationList.xml.aspx'

    insertData = []
    downloadedData = urllib.urlopen(apiURL)

    #Parse the data into the headers and lines of data
    XMLData = minidom.parse(downloadedData)
    headerNode = XMLData.getElementsByTagName("rowset")[0]
    columnHeaders = headerNode.attributes['columns'].value.split(',')
    dataNodes = XMLData.getElementsByTagName("row")
    
    for row, dataNode in enumerate(dataNodes):
        if TERM_OUT == True:
            print "sID: ", dataNode.attributes['stationID'].value, "sName: ", dataNode.attributes['stationName'].value, "sSID: ", dataNode.attributes['solarSystemID'].value
        sql = "SELECT constellationID, regionID FROM eve_sdd.mapSolarSystems WHERE solarSystemID=%s" % dataNode.attributes['solarSystemID'].value
        curs.execute(sql)
        row = curs.fetchone()
        dataRow = (dataNode.attributes['stationID'].value, dataNode.attributes['stationName'].value, dataNode.attributes['solarSystemID'].value, dataNode.attributes['corporationID'].value, dataNode.attributes['stationTypeID'].value, row[0], row[1])
        insertData.append(dataRow)
        
    if len(insertData)>0:
        sql = "REPLACE INTO eve_sdd.staStations (stationID, stationName, solarSystemID, corporationID, stationTypeID, constellationID, regionID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        curs.executemany(sql, insertData)
        
    dbcon.commit()
    
if __name__ == '__main__':
    main()
