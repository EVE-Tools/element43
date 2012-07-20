#!/usr/bin/env python
"""
Get the data from EMDR and shove it into the database
Greg Oberfield gregoberfield@gmail.com

TODO:
1. Documentation
2. History message processing (sort of done: 7/20/12)
3. wrap try/catch blocks around SQL statements
4. cleaner date processing - pgsql supports timezones whereas Mysql did not so it's a little hokey right now
5. move settings to external file so I don't have to keep changing them

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
import base64

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 75

# DEBUG flag
DEBUG = False

# If you want terminal output
TERM_OUT = True

# database stuff
redisdb = "localhost"

# use a greenlet pool to cap the number of workers at a reasonable level
greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)

queue = HotQueue("emdr-messages", host=redisdb, port=6379, db=0)
dbcon = psycopg2.connect("host=192.168.1.41 user=element43 host=192.168.1.41 password=element43")
dbcon.autocommit = True

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
                #curs.execute(sql)
                row = (abs(hash(str(item_region_list.region_id)+str(item_region_list.type_id))), item_region_list.type_id, item_region_list.region_id, 0)
                insertEmpty.append(row)
                row = (abs(hash(str(item_region_list.region_id)+str(item_region_list.type_id)))+1, item_region_list.type_id, item_region_list.region_id, 1)
                insertEmpty.append(row)
                row = (0,)
                statsData.append(row)
            """
            for components in insertEmpty:
                try:
                    sql = "INSERT IGNORE INTO seenOrders (orderID, typeID, regionID, bid) values (%s, %s, %s, %s)" % components
                    curs.execute(sql)
                except psycopg2.DatabaseError, e:
                    if TERM_OUT == True:
                        print "Key collision: ", components
            """
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
                            bid = True
                        else:
                            bid = False
                        
                        # Check order if "supicious" which is an arbitrary definition.  Any orders that are outside 2 standard deviations
                        # of the mean AND where there are more than 5 orders of like type in the station will be flagged.  Flagging could
                        # be done on a per-web-request basis but doing it on order entry means you can report a little more on it.
                        # Flags: 'Y' = Yes (suspicious), 'N' = No (not suspicious), '?' or NULL = not enough information to determine
                        suspicious = False
                        if (order.type_id!=statTypeID) or (order.station_id!=statStationID):
                            gevent.sleep()
                            sql = "SELECT COUNT(id), STDDEV(price), AVG(price) FROM market_data_orders WHERE type_id=%s AND station_id=%s" % (order.type_id, order.station_id)
                            statTypeID = order.type_id
                            statStationID = order.station_id
                            recordCount = None
                            curs.execute(sql)
                            result = curs.fetchone()
                            if result:
                                recordCount = result[0]
                                if recordCount!=None:
                                    stddev = result[1]
                                    mean = result[2]
                                suspicious = False
                                if (stddev!=None) and (recordCount > 5):
                                    # if price is outside 2 standard deviations of the mean flag as suspicious
                                    if float(abs(order.price - mean)) > (2*stddev):
                                        suspicious = True
                    
                        # See if the order already exists, if so, update if needed otherwise insert                
                        sql = "SELECT * FROM market_data_orders WHERE id = %s" % order.order_id
                        curs.execute(sql)
                        result = curs.fetchone()
                        if result:
                            foundOrder = result
                            row=(2,)
                            statsData.append(row)
                            if orderHash != hashlib.md5(str(foundOrder[8])+str(foundOrder[3])+str(foundOrder[4])).hexdigest():
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
                sql = "UPDATE market_data_orders SET generated_at=%s WHERE id = %s"
                curs.executemany(sql, updateData)
                updateData = []
    
            if len(insertData)>0:
                # Build our SQL statement
                if TERM_OUT==True:
                    print "--- INSERTING "+str(len(insertData))+" (UPDATES: "+str(updateCounter)+") ORDERS ---"
                #print insertData
                sql = "INSERT INTO market_data_orders (id,"
                sql += "type_id, station_id, solar_system_id, region_id, is_bid, price, order_range,"
                sql += "duration, volume_remaining, volume_entered, minimum_volume, generated_at,"
                sql += "issue_date, message_key, is_suspicious, uploader_ip_hash) values (%s, %s, %s, %s, %s, %s, %s, %s,"
                sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                
                curs.executemany(sql, insertData)
                insertData = []
    
            if duplicateData:
                if TERM_OUT==True:
                    print "*** DUPLICATES: "+str(duplicateData)+" ORDERS ***"
    
            """
            if len(insertSeen)>0:
                sql = "INSERT IGNORE INTO seenOrders (orderID, typeID, regionID) values (%s, %s, %s)"
                curs.executemany(sql, insertSeen)
                insertSeen = []
            
            if DEBUG==True:        
                msgType = "emdr"
                query.query("INSERT INTO `emdrJsonmessages` (msgKey, msgType, message) VALUES (%s, %s, %s)",(msgKey, msgType, message))
            """
            
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
            uniqueKey = str(history.region_id)+"-"+str(history.type_id)
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
            sql = "SELECT * FROM market_data_history WHERE id = '%s'" % uniqueKey
            curs.execute(sql)
            result = curs.fetchone()
            #print "Result: ", result
            if result:
                checkHash = hash(str(data))
                decodedData = ast.literal_eval(zlib.decompress(base64.standard_b64decode(result[3])))
                #print base64.decodestring(zlib.decompress(result[3]))
                #decodedData.update(data)
                data.update(decodedData)
                encodedData = base64.standard_b64encode(zlib.compress(json.dumps(data)))
                sql = "UPDATE market_data_history SET history_data='%s' WHERE id = '%s'" % (encodedData, uniqueKey)
                if TERM_OUT==True:
                    print "### UPDATING " + str(rowCount) + " HISTORY RECORDS ###"
            elif len(data)>0:
                encodedData = base64.standard_b64encode(zlib.compress(json.dumps(data)))
                sql = "INSERT INTO market_data_history (id, region_id, type_id, history_data) VALUES ('%s', %s, %s, '%s')" % (uniqueKey, regionID, typeID, encodedData)

                if TERM_OUT==True:
                    print "### INSERTING " + str(rowCount) + " HISTORY RECORDS ###"

            if hash(str(data))!=checkHash:
                #print "region: ", regionID, "type: ", typeID
                curs.execute(sql)
                # If we need to debug raw messages (commented out for now to save space)
                if DEBUG==True:
                    msgType = "emdr"
                    #query.query("INSERT INTO `emdrJsonmessages` (msgKey, msgType, message) VALUES (%s, %s, %s)",(msgKey, msgType, message))
            elif TERM_OUT==True:
                print "^^^ DUPLICATED HISTORY ^^^"

    gevent.sleep()
    
    """
    try:
        sql = "INSERT INTO emdrStatsWorking (statusType) VALUES (%s)"
        curs.executemany(sql, statsData)
    except psycopg2.DatabaseError, e:
        if TERM_OUT == True:
            print "Key collision: ", statsData
    """
    
if __name__ == '__main__':
    main()

