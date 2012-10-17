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
from datetime import date
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
import ConfigParser
import os
import pylibmc
import numpy.ma as ma
import numpy as np
from scipy.stats import scoreatpercentile

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read(['consumer.conf', 'local_consumer.conf'])
dbhost = config.get('Database', 'dbhost')
dbname = config.get('Database', 'dbname')
dbuser = config.get('Database', 'dbuser')
dbpass = config.get('Database', 'dbpass')
dbport = config.get('Database', 'dbport')
redisdb = config.get('Redis', 'redishost')
max_order_age = config.getint('Consumer', 'max_order_age')
DEBUG = config.getboolean('Consumer', 'debug')
TERM_OUT = config.getboolean('Consumer', 'term_out')
mcserver = config.get('Memcache', 'server')
mckey = config.get('Memcache', 'key')
statkey = config.get('Memcache', 'statkey')

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 75

# item list of stuff we want immediately updated in stats
fastupdate = [34, 35, 36, 37, 38, 39, 40, 29668]

# use a greenlet pool to cap the number of workers at a reasonable level
greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)

queue = HotQueue("emdr-messages", host=redisdb, port=6379, db=0)
statqueue =  HotQueue("e43-stats", host=redisdb, port=6379, db=0)

# Handle DBs without password
if not dbpass:
    # Connect without password
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" dbname="
                             +dbname+" port="+dbport)
else:
    dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass
                             +" dbname="+dbname+" port="+dbport)
    
#connect to memcache
mc = pylibmc.Client([mcserver], binary=True,
                    behaviors={"tcp_nodelay": True, "ketama": True})
    
dbcon.autocommit = True

def main():
    for message in queue.consume():
        #print ">>> spawning"
        greenlet_pool.spawn(thread, message)
        
def stats(item, region):
    """
    grab the dictionary and process for that region/item combo
    """
    buyprice = []
    sellprice = []
    buycount = []
    sellcount = []
    item_stats = {}
    buyavg = 0
    buymean = 0
    sellavg = 0
    sellmean = 0
    buymedian = 0
    sellmedian = 0
    buyvolume = 0
    sellvolume = 0
    buy_95_percentile = 0
    sell_95_percentile = 0
    timestamp = date.today()
        
    curs = dbcon.cursor()

    # get the current record so we can compare dates and see if we
    # need to move current records to the history table (this is for history use)
    sql = """SELECT buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, buyvolume, sellvolume,
                buy_95_percentile, sell_95_percentile, lastupdate
                FROM market_data_itemregionstat
                WHERE mapregion_id = %s AND invtype_id = %s""" % (region, item)
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print "Error: ", e
        print "SQL: ", sql
    history = curs.fetchone()
    # Grab all the live orders for this item/region combo
    sql = """SELECT price, is_bid, volume_remaining
                FROM market_data_orders
                WHERE mapregion_id = %s AND invtype_id = %s AND is_active = 't'""" % (region, item)
    curs.execute(sql)
    for record in curs:
        # Depending on buy/sell status,
        # append to the proper list pricing and volume
        if record[1] == False:
            sellprice.append(record[0])
            sellcount.append(record[2])
        else:
            buyprice.append(record[0])
            buycount.append(record[2])
            
    # process the buy side
    if len(buyprice) > 1:
        top = scoreatpercentile(buyprice, 95)
        bottom = scoreatpercentile(buyprice, 5)
        # mask out the bottom 5% of orders so we can try to eliminate the BS
        buy_masked = ma.masked_outside(buyprice, bottom, top)
        tempmask = buy_masked.mask
        buycount_masked = ma.array(buycount, mask=tempmask, fill_value = 0)
        ma.fix_invalid(buy_masked, mask=0)
        ma.fix_invalid(buycount_masked, mask=0)
        buyavg = np.nan_to_num(ma.average(buy_masked, 0, buycount_masked))
        buymean = np.nan_to_num(ma.mean(buy_masked))
        buymedian = np.nan_to_num(ma.median(buy_masked))
        buy_95_percentile = top
        if len(buyprice) < 4:
            buyavg = np.nan_to_num(ma.average(buyprice))
            buymean = np.nan_to_num(ma.mean(buyprice))
        buyprice.sort()
        buy = buyprice.pop()
        
    # same processing for sell side as buy side
    if len(sellprice) > 1:
        top = scoreatpercentile(sellprice, 95)
        bottom = scoreatpercentile(sellprice, 5)
        sell_masked = ma.masked_outside(sellprice, bottom, top)
        tempmask = sell_masked.mask
        sellcount_masked = ma.array(sellcount, mask=tempmask, fill_value = 0)
        ma.fix_invalid(sell_masked, mask=0)
        ma.fix_invalid(sellcount_masked, mask=0)
        sellavg = np.nan_to_num(ma.average(sell_masked, 0, sellcount_masked))
        sellmean = np.nan_to_num(ma.mean(sell_masked))
        sellmedian = np.nan_to_num(ma.median(sell_masked))
        sell_95_percentile = bottom
        if len(sellprice) < 4:
            sellAvg = np.nan_to_num(ma.average(sellprice))
            sellMean = np.nan_to_num(ma.mean(sellprice))
        sellprice.sort()
        sell = sellprice.pop()
    
    # process for history
    if (history is not None) and (history[10] is not None):
        if history[10].date() != timestamp:
            if (TERM_OUT==True):
                print "--- New date, new insert", region, " / ", item, "(", history[10].date(), " - ", timestamp, ")"
            # dates differ, need to move the data
            sql = """INSERT INTO market_data_itemregionstathistory
                        (buymean, buyavg, buymedian, sellmean, sellavg,
                        sellmedian, buyvolume, sellvolume, buy_95_percentile, sell_95_percentile, mapregion_id, invtype_id, date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')""" % (history[0],
                                                                                            history[1],
                                                                                            history[2],
                                                                                            history[3],
                                                                                            history[4],
                                                                                            history[5],
                                                                                            history[6],
                                                                                            history[7],
                                                                                            history[8],
                                                                                            history[9],
                                                                                            region,
                                                                                            item,
                                                                                            history[10])
            try:
                curs.execute(sql)
            except psycopg2.DatabaseError, e:
                print "Error: ", e
                print "SQL: ", sql
        elif (TERM_OUT==True):
            print "/// Timestamps match:", region, " / ", item, "(", history[10].date(), " - ", timestamp, ")"
    else:
        if (TERM_OUT==True):
            print "--- No history, new insert", region, " / ", item
        sql = """INSERT INTO market_data_itemregionstathistory (buymean, buyavg, buymedian, sellmean,
                    sellavg, sellmedian, buyvolume, sellvolume, buy_95_percentile, sell_95_percentile, mapregion_id, invtype_id, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    '%s')""" % (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, sum(buycount), sum(sellcount), buy_95_percentile, sell_95_percentile, region, item, timestamp)
        try:
            curs.execute(sql)
        except psycopg2.DatabaseError, e:
            print "Error: ", e
            print "SQL: ", sql
        
    # if it's an item in fastupdate, stick it in the cache
    if item in fastupdate:
        item_stats['buyavg']=buyavg
        item_stats['sellavg'] = sellavg
        item_stats['buymedian'] = buymedian
        item_stats['sellmedian'] = sellmedian
        mc.set(statkey + str(item), json.dumps(item_stats), time=86400)
        #print "CACHE INSERT: ", item, "[", item_stats['buyavg'], " / ", item_stats['sellavg'], "]"
        
    # insert it into the DB or update if already exists
    if history == None:
        sql = """INSERT INTO market_data_itemregionstat (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian,
                    buyvolume, sellvolume, buy_95_percentile, sell_95_percentile, mapregion_id, invtype_id, lastupdate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')""" % (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian,
                                                                                        sum(buycount), sum(sellcount), buy_95_percentile, sell_95_percentile, region, item, timestamp)
    else:
        sql = """UPDATE market_data_itemregionstat SET buymean = %s, buyavg = %s, buymedian = %s, sellmean = %s, sellavg = %s, sellmedian = %s,
                    buyvolume = %s, sellvolume = %s, buy_95_percentile = %s, sell_95_percentile = %s, lastupdate = '%s'
                    WHERE mapregion_id = %s AND invtype_id = %s""" % (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian,
                                                                      sum(buycount), sum(sellcount), buy_95_percentile, sell_95_percentile, timestamp, region, item)
    #print sql
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print "Error: ", e
        print "SQL: ", sql
        
    dbcon.commit()

def thread(message):
    """
    main flow of the app
    """
    #print "<<< entered thread"
    curs = dbcon.cursor()

    mc = pylibmc.Client([mcserver], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

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
        row=(5,)
        statsData.append(row)
        sql = ""
        #print "* Recieved Orders from: %s" % market_list.order_generator
        statTypeID = 0
        statRegionID = 0
        oldCounter = 0
        ipHash = None
        for uploadKey in market_list.upload_keys:
            if uploadKey['name'] == 'EMDR':
                ipHash = uploadKey['key']
        # empty order (no buy or sell orders)
        if len(market_list)==0:
            for item_region_list in market_list._orders.values():
                if TERM_OUT==True:
                    print "NO ORDERS for region: ", item_region_list.region_id, " item: ", item_region_list.type_id
                row = (abs(hash(str(item_region_list.region_id)+str(item_region_list.type_id))), item_region_list.type_id, item_region_list.region_id)
                insertEmpty.append(row)
                row = (0,)
                statsData.append(row)
            
            for components in insertEmpty:
                if mckey + str(components[0]) in mc:
                    continue
                try:
                    sql = "SELECT id FROM market_data_orders WHERE id = %s and is_active='f'" % components[0]
                    curs.execute(sql)
                    result = curs.fetchone()
                    if result is not None:
                        continue
                    sql = "INSERT INTO market_data_seenorders (id, type_id, region_id) values (%s, %s, %s)" % components
                    curs.execute(sql)
                    mc.set(mckey + str(components[0]), True, time=2)
                except psycopg2.DatabaseError, e:
                    if TERM_OUT == True:
                        print "Key collision: ", components
        # at least some results to process    
        else:
            for item_region_list in market_list.get_all_order_groups():
                for order in item_region_list:
                    # if order is in the future, skip it
                    if order.generated_at > now_dtime_in_utc():
                        if TERM_OUT==True:
                            print "000 Order has gen_at in the future 000"
                        continue
                    issue_date = str(order.order_issue_date).split("+", 1)[0]
                    generated_at = str(order.generated_at).split("+", 1)[0]
                    if (order.generated_at > (now_dtime_in_utc() - datetime.timedelta(hours=max_order_age))):                   
                        # convert the bid true/false to binary
                        if order.is_bid:
                            bid = True
                        else:
                            bid = False
                        
                        # Check to see if the order is in the warehouse when it shouldn't be, just in case    
                        sql = "SELECT id FROM market_data_orders WHERE id = %s and is_active='f'" % order.order_id
                        curs.execute(sql)
                        result = curs.fetchone()
                        if result is not None:
                            if TERM_OUT==True:
                                print "/// Bad order archived, ID: %s Region: %s TypeID: %s ///" % (order.order_id, order.region_id, order.type_id)
                                sql = "UPDATE market_data_orders SET is_active='t' WHERE id = %s" % order.order_id
                                try:
                                    curs.execute(sql)
                                    continue
                                except psycopg2.DatabaseError, e:
                                    if TERM_OUT == True:
                                        print "&^&^ Update status FAILED:", e
                        # Check order if "supicious" which is an arbitrary definition.  Any orders that are outside 2 standard deviations
                        # of the mean AND where there are more than 5 orders of like type in the region will be flagged.  Flagging could
                        # be done on a per-web-request basis but doing it on order entry means you can report a little more on it.
                        # Flags: True = Yes (suspicious), False = No (not suspicious), NULL = not enough information to determine
                        suspicious = False
                        if (order.type_id!=statTypeID) or (order.region_id!=statRegionID):
                            gevent.sleep()
                            sql = "SELECT COUNT(id), STDDEV(price), AVG(price) FROM market_data_orders WHERE invtype_id=%s AND mapregion_id=%s" % (order.type_id, order.region_id)
                            statTypeID = order.type_id
                            statRegionID = order.region_id
                            recordCount = None
                            curs.execute(sql)
                            result = curs.fetchone()
                            if result:
                                recordCount = result[0]
                                if recordCount!=None:
                                    stddev = result[1]
                                    mean = result[2]
                                if (stddev!=None) and (recordCount > 3):
                                    # if price is outside 1 standard deviation of the mean flag as suspicious 
                                    if ((float(order.price - mean)) > stddev) or ((float(order.price - mean)) < stddev):
                                        if bid and (order.price < mean):
                                            suspicious = True
                                        elif not bid and (order.price > mean):
                                            suspicious = True
                    
                        # See if the order already exists, if so, update if needed otherwise insert                
                        sql = "SELECT * FROM market_data_orders WHERE id = %s" % order.order_id
                        curs.execute(sql)
                        result = curs.fetchone()
                        if result:
                            if result[0] < order.generated_at:
                                row=(2,)
                                statsData.append(row)
                                row = (order.price, order.volume_remaining, order.generated_at, issue_date, msgKey, suspicious, ipHash, order.order_id)
                                updateData.append(row)
                            else:
                                if TERM_OUT==True:
                                    print "||| Older order, not updated |||"
                        else:
                            # set up the data insert for the specific order
                            row = (1,)
                            statsData.append(row)
                            row = (order.order_id, order.type_id, order.station_id, order.solar_system_id,
                                order.region_id, bid, order.price, order.order_range, order.order_duration,
                                order.volume_remaining, order.volume_entered, order.minimum_volume, order.generated_at, issue_date, msgKey, suspicious, ipHash)
                            insertData.append(row)
                            updateCounter += 1
                        row = (order.order_id, order.type_id, order.region_id)
                        if mckey + str(row[0]) in mc:
                            continue
                        insertSeen.append(row)
                        mc.set(mckey + str(row[0]), True, time=2)
                        stats(order.type_id, order.region_id)
                    else:
                        oldCounter += 1
                        row = (3,)
                        statsData.append(row)
                        
            if TERM_OUT==True:
                if (oldCounter>0):
                    print "<<< ", oldCounter, "OLD ORDERS >>>"
    
            if len(updateData)>0:
                if TERM_OUT==True:
                    print "::: UPDATING "+str(len(updateData))+" ORDERS :::"
                sql = "UPDATE market_data_orders SET price=%s, volume_remaining=%s, generated_at=%s, issue_date=%s, message_key=%s, is_suspicious=%s, uploader_ip_hash=%s WHERE id = %s"
                curs.executemany(sql, updateData)
                updateData = []
    
            if len(insertData)>0:
                # Build our SQL statement
                if TERM_OUT==True:
                    print "--- INSERTING "+str(len(insertData))+" ORDERS ---"
                #print insertData
                sql = "INSERT INTO market_data_orders (id, invtype_id, stastation_id, mapsolarsystem_id, mapregion_id,"
                sql += "is_bid, price, order_range, "
                sql += "duration, volume_remaining, volume_entered, minimum_volume, generated_at, "
                sql += "issue_date, message_key, is_suspicious, uploader_ip_hash, is_active) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 't')"
                
                curs.executemany(sql, insertData)
                insertData = []
    
            if duplicateData:
                if TERM_OUT==True:
                    print "*** DUPLICATES: "+str(duplicateData)+" ORDERS ***"
    
            if len(insertSeen)>0:
                try:
                    sql = "INSERT INTO market_data_seenorders (id, type_id, region_id) values (%s, %s, %s)"
                    curs.executemany(sql, insertSeen)
                except psycopg2.DatabaseError, e:
                    if TERM_OUT==True:
                        print e.pgerror
                insertSeen = []
            
            if DEBUG==True:        
                msgType = "emdr"
                curs.execute("INSERT INTO `emdrJsonmessages` (msgKey, msgType, message) VALUES (%s, %s, %s)",(msgKey, msgType, message))
            
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
        row = (4,)
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
                decodedData = ast.literal_eval(result[1])
                data.update(decodedData)
                encodedData = json.dumps(data)
                sql = "UPDATE market_data_history SET history_data='%s' WHERE id = '%s'" % (encodedData, uniqueKey)
                if TERM_OUT==True:
                    print "### UPDATING " + str(rowCount) + " HISTORY RECORDS ###"
            elif len(data)>0:
                encodedData = json.dumps(data)
                sql = "INSERT INTO market_data_history (id, mapregion_id, invtype_id, history_data) VALUES ('%s', %s, %s, '%s')" % (uniqueKey, regionID, typeID, encodedData)

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
    
    try:
        sql = "INSERT INTO market_data_emdrstatsworking (status_type) VALUES (%s)"
        curs.executemany(sql, statsData)
    except psycopg2.DatabaseError, e:
        if TERM_OUT == True:
            print "Key collision: ", statsData
    
if __name__ == '__main__':
    main()

