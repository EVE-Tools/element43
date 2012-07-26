#!/usr/bin/env python
"""
Get the conquerable station list from the API and load it into the SDD database
Greg Oberfield gregoberfield@gmail.com
"""

import psycopg2
import urllib
from xml.dom import minidom
import ConfigParser
import os
import pylibmc

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read(['consumer.conf', 'local_consumer.conf'])
dbhost = config.get('Database', 'dbhost')
dbname = config.get('Database', 'dbname')
dbuser = config.get('Database', 'dbuser')
dbpass = config.get('Database', 'dbpass')
dbport = config.get('Database', 'dbport')
DEBUG = config.getboolean('Consumer', 'debug')
TERM_OUT = config.getboolean('Consumer', 'term_out')


def main():
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)
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
        sql = "DELETE FROM eve_db_stastation WHERE id=%s" % dataNode.attributes['stationID'].value
        curs.execute(sql)
        if TERM_OUT == True:
            print "sID: ", dataNode.attributes['stationID'].value, "sName: ", dataNode.attributes['stationName'].value, "sSID: ", dataNode.attributes['solarSystemID'].value
        sql = "SELECT constellation_id, region_id FROM eve_db_mapsolarsystem WHERE id=%s" % dataNode.attributes['solarSystemID'].value
        curs.execute(sql)
        row = curs.fetchone()
        dataRow = (dataNode.attributes['stationID'].value, dataNode.attributes['stationName'].value, dataNode.attributes['solarSystemID'].value, dataNode.attributes['stationTypeID'].value, row[0], row[1])
        insertData.append(dataRow)
        
    if len(insertData)>0:
        sql = "INSERT INTO eve_db_stastation (id, name, solar_system_id, type_id, constellation_id, region_id) VALUES (%s, %s, %s, %s, %s, %s)"
        curs.executemany(sql, insertData)
        
    dbcon.commit()
    
if __name__ == '__main__':
    main()
