#!/usr/bin/env python
"""
Get the data from EMDR and shove it into the database
Greg Oberfield gregoberfield@gmail.com
"""

from emds.formats import unified
from emds.common_utils import now_dtime_in_utc
import zlib
import datetime
import dateutil.parser
import pytz
import sys
import uuid
import ujson as json
# Need ast to convert from string to dictionary
import ast
from hotqueue import HotQueue
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
import psycopg2
import hashlib

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 75

# DEBUG flag
DEBUG = False

# If you want terminal output
TERM_OUT = True

# database stuff
redisdb = "localhost"
dbhost="localhost"
dbname = "dbname"
dbuser = "dbuser"
dbpass = "dbpass"

# use a greenlet pool to cap the number of workers at a reasonable level
greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)

queue = HotQueue("emdr-messages", host=redisdb, port=6379, db=0)
dbcon = psycopg2.connect("host=192.168.1.41 user=element43 host=192.168.1.41 password=element43")

def main():
    for message in queue.consume():
        #print ">>> spawning"
        greenlet_pool.spawn(thread, message)

def thread(message):
    """
    main flow of the app
    """
    #print "<<< entered thread"
    curs = dbcon.cursor()

    market_json = zlib.decompress(message)
    market_list = unified.parse_from_json(market_json)
    # Create unique identified for this message if debug is true
    if DEBUG==True:
        msgKey = str(uuid.uuid4())
    else:
        msgKey = ""

    #print "<<- parsed message"

    if market_list.list_type == 'orders':
        #print "* Recieved Orders from: %s" % market_list.order_generator
        insertData = []       # clear the data structures
        updateData = []
        insertSeen = []
        insertEmpty = []
        updateCounter = 0
        duplicateData = 0
        hashList = []
        statsData = []
        sql = ""
        orderHash = 0
        #print "* Recieved Orders from: %s" % market_list.order_generator
        statTypeID = 0
        statStationID = 0
        oldCounter = 0
        ipHash = None
        for uploadKey in market_list.upload_keys:
            if uploadKey['name'] == 'EMDR':
                ipHash = uploadKey['key']
                if TERM_OUT == True:
                    print "IP Hash: ", ipHash
        if len(market_list)==0:
            for item_region_list in market_list._orders.values():
                if TERM_OUT==True:
                    print "NO ORDERS for region: ", item_region_list.region_id, " item: ", item_region_list.type_id
                sql = "SELECT * FROM seenOrders WHERE orderID = %s" % (abs(hash(str(item_region_list.region_id)+str(item_region_list.type_id)))+1)
                curs.execute(sql)
                row = (abs(hash(str(item_region_list.region_id)+str(item_region_list.type_id))), item_region_list.type_id, item_region_list.region_id, 0)
                insertEmpty.append(row)
                row = (abs(hash(str(item_region_list.region_id)+str(item_region_list.type_id)))+1, item_region_list.type_id, item_region_list.region_id, 1)
                insertEmpty.append(row)
                row = (0,)
                statsData.append(row)
            for components in insertEmpty:
                try:
                    sql = "INSERT IGNORE INTO seenOrders (orderID, typeID, regionID, bid) values (%s, %s, %s, %s)" % components
                    curs.execute(sql)
                except psycopg2.DatabaseError, e:
                    if TERM_OUT == True:
                        print "Key collision: ", components
        else:
            for item_region_list in market_list.get_all_order_groups():
                for order in item_region_list:
                    # set up the dates so MySQL won't barf
                    issue_date = str(order.order_issue_date).split("+", 1)[0]
                    generated_at = str(order.generated_at).split("+", 1)[0]
                    if (order.generated_at > (now_dtime_in_utc() - datetime.timedelta(hours=8))):
                    #if True:
                        orderHash = hashlib.md5(str(order.order_id)+str(order.price)+str(order.volume_remaining)).hexdigest()
                        
                        # convert the bid true/false to binary
                        if order.is_bid:
                            bid = 1
                        else:
                            bid = 0
                        
                        # Check order if "supicious" which is an arbitrary definition.  Any orders that are outside 2 standard deviations
                        # of the mean AND where there are more than 5 orders of like type in the station will be flagged.  Flagging could
                        # be done on a per-web-request basis but doing it on order entry means you can report a little more on it.
                        # Flags: 'Y' = Yes (suspicious), 'N' = No (not suspicious), '?' or NULL = not enough information to determine
                        suspicious = '?'
                        if (order.type_id!=statTypeID) or (order.station_id!=statStationID):
                            gevent.sleep()
                            sql = "SELECT COUNT(orderID), STDDEV(price), AVG(price) FROM marketData WHERE typeID=%s AND stationID=%s" % (order.type_id, order.station_id)
                            statTypeID = order.type_id
                            statStationID = order.station_id
                            recordCount = None
                            curs.execute(sql)
                            result = curs.fetchone()
                            if result:
                                recordCount = result[0]
                                if recordCount!=None:
                                    stddev = resultRow[1]
                                    mean = resultRow[2]
                                suspicious = 'N'
                                if (stddev!=None) and (recordCount > 5):
                                    # if price is outside 2 standard deviations of the mean flag as suspicious
                                    if float(abs(order.price - mean)) > (2*stddev):
                                        suspicious = 'Y'
                                else:
                                    suspicious = '?'
                    
                        # See if the order already exists, if so, update if needed otherwise insert                
                        sql = "SELECT * FROM marketData WHERE orderID = %s" % order.order_id
                        curs.execute(sql)
                        result = curs.fetchone()
                        if result:
                            foundOrder = result
                            row=(2,)
                            statsData.append(row)
                            if orderHash != hashlib.md5(str(foundOrder[0]['orderID'])+str(foundOrder[0]['price'])+str(foundOrder[0]['volumeRemaining'])).hexdigest():
                                row = (order.order_id, order.type_id, order.station_id, order.solar_system_id,
                                       order.region_id, bid, order.price, order.order_range, order.order_duration,
                                       order.volume_remaining, order.volume_entered, order.minimum_volume, generated_at, issue_date, msgKey, suspicious, ipHash)
                                insertData.append(row)
                            else:
                                row = (generated_at, order.order_id)
                                updateData.append(row)
                        else:
                            # set up the data insert for the specific order
                            row = (1,)
                            statsData.append(row)
                            row = (order.order_id, order.type_id, order.station_id, order.solar_system_id,
                                order.region_id, bid, order.price, order.order_range, order.order_duration,
                                order.volume_remaining, order.volume_entered, order.minimum_volume, generated_at, issue_date, msgKey, suspicious, ipHash)
                            insertData.append(row)
                            updateCounter = updateCounter + 1
                        row = (order.order_id, order.type_id, order.region_id)
                        insertSeen.append(row)
                    else:
                        oldCounter = oldCounter+1
                        row = (3,)
                        statsData.append(row)
                        
            if TERM_OUT==True:
                if (oldCounter>0):
                    print "<<< ", oldCounter, "OLD ORDERS >>>"
    
            if len(updateData)>0:
                if TERM_OUT==True:
                    print "--- UPDATING "+str(len(updateData))+" ORDERS ---"
                sql = "UPDATE marketData SET marketData.generatedAt=%s WHERE orderID = %s"
                curs.executemany(sql, updateData)
                updateData = []
    
            if len(insertData)>0:
                # Build our SQL statement
                if TERM_OUT==True:
                    print "--- INSERTING "+str(len(insertData))+" (UPDATES: "+str(updateCounter)+") ORDERS ---"
                #print insertData
                sql = "REPLACE INTO marketData (`orderID`,"
                sql = sql + "`typeID`, `stationID`, `solarSystemID`, `regionID`, `bid`, `price`, `range`,"
                sql = sql + "`duration`, `volumeRemaining`, `volumeEntered`, `minimumVolume`, `generatedAt`,"
                sql = sql + "`issueDate`, `msgKey`, `suspicious`, `ipHash`) values (%s, %s, %s, %s, %s, %s, %s, %s,"
                sql = sql + "%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
                if duplicateData:
                    if TERM_OUT==True:
                        print "*** DUPLICATES: "+str(duplicateData)+" ORDERS ***"
    
                curs.executemany(sql, insertData)
                insertData = []

            if len(insertSeen)>0:
                sql = "INSERT IGNORE INTO seenOrders (orderID, typeID, regionID) values (%s, %s, %s)"
                curs.executemany(sql, insertSeen)
                insertSeen = []
            
            if DEBUG==True:        
                msgType = "emdr"
                query.query("INSERT INTO `emdrJsonmessages` (msgKey, msgType, message) VALUES (%s, %s, %s)",(msgKey, msgType, message))
    
    elif market_list.list_type == 'history':
        data = {}
        rowCount = 0
        encodedData = {}
        decodedData = {}
        statsData = []
        uniqueKey = ""
        rows = []
        regionID = 0
        checkHash = 0
        row = (4)
        statsData.append(row)
        for history in market_list.get_all_entries_ungrouped():
            rowCount = rowCount+1
            # Process the history rows
            date = str(history.historical_date).split("+", 1)[0]
            todayDate = now_dtime_in_utc().date()
            theDate = history.historical_date.date()
            generatedAt = str(history.generated_at).split("+", 1)[0]
            if uniqueKey == "":
                keyBuilder = str(history.region_id)+"-"+str(history.type_id)
                uniqueKey = uuid.uuid5(uuid.NAMESPACE_DNS, keyBuilder)
                regionID = history.region_id
                typeID = history.type_id
            if todayDate!=theDate:
                # clip the high and low if it's an order of magnitude too high or low to cut out the idiots
                if history.high_price > (history.average_price*10):
                    history.high_price = history.average_price*10
                if history.low_price < (history.average_price/10):
                    history.low_price = history.average_price/10
                data[date] = [history.num_orders, history.low_price, history.high_price, history.average_price, history.total_quantity, msgKey]
        
        if regionID!=0:
            sql = "SELECT * FROM historicalData WHERE `uniqueKey` = '%s'" % uniqueKey
            curs.execute(sql)
            result = curs.fetchone()
            if result:
                rows = result
                checkHash = hash(str(data))
                decodedData = ast.literal_eval(zlib.decompress(result[3]))
                #decodedData.update(data)
                data.update(decodedData)
                encodedData = zlib.compress(json.dumps(data))
                sql = "UPDATE historicalData SET `historyData`=%s WHERE `uniqueKey` = %s"
                params = (encodedData, uniqueKey)
                if TERM_OUT==True:
                    print "### UPDATING " + str(rowCount) + " HISTORY RECORDS ###"
            elif len(data)>0:
                encodedData = zlib.compress(json.dumps(data))
                sql = "INSERT INTO historicalData (`uniqueKey`, `regionId`, `typeID`, `historyData`) VALUES (%s, %s, %s, %s)"
                params = (uniqueKey, regionID, typeID, encodedData)

                if TERM_OUT==True:
                    print "### INSERTING " + str(rowCount) + " HISTORY RECORDS ###"

            if hash(str(data))!=checkHash:
                #print "region: ", regionID, "type: ", typeID
                query.query(sql, params)
                # If we need to debug raw messages (commented out for now to save space)
                if DEBUG==True:
                    msgType = "emdr"
                    query.query("INSERT INTO `emdrJsonmessages` (msgKey, msgType, message) VALUES (%s, %s, %s)",(msgKey, msgType, message))
            elif TERM_OUT==True:
                print "^^^ DUPLICATED HISTORY ^^^"

    gevent.sleep()
    sql = "INSERT INTO emdrStatsWorking (statusType) VALUES (%s)"
    curs.executemany(sql, statsData)
    curs.commit()

if __name__ == '__main__':
    main()

