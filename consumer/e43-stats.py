#!/usr/bin/env python
"""
Go through the database and calculate stats for item/region combos
based on seen from warehouse script
Greg Oberfield gregoberfield@gmail.com
"""

import gevent
import ConfigParser
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
from hotqueue import HotQueue
import psycopg2
import numpy.ma as ma
import numpy as np
import scipy.stats as stats
import datetime
from datetime import date

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read(['consumer.conf', 'local_consumer.conf'])
redisdb = config.get('Redis', 'redishost')
dbhost = config.get('Database', 'dbhost')
dbname = config.get('Database', 'dbname')
dbuser = config.get('Database', 'dbuser')
dbpass = config.get('Database', 'dbpass')
dbport = config.get('Database', 'dbport')
DEBUG = config.getboolean('Consumer', 'debug')
TERM_OUT = config.getboolean('Consumer', 'term_out')

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 10

# use a greenlet pool to cap the number of workers at a reasonable level
greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)

queue =  HotQueue("e43-stats", host=redisdb, port=6379, db=0)
dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)
dbcon.autocommit = True

def main():
    for message in queue.consume():
        #print ">>> spawning"
        greenlet_pool.spawn(thread, message)
        
def thread(data):
    """
    grab the dictionary and process for that region/item combo
    """
    buyprice = []
    sellprice = []
    buycount = []
    sellcount = []
    buyavg = 0
    buymean = 0
    sellavg = 0
    sellmean = 0
    buymedian = 0
    sellmedian = 0
    timestamp = date.today()
    
    curs = dbcon.cursor()

    # get the current record so we can compare dates and see if we need to move current records to the history table (this is for history use)
    sql = "SELECT buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, lastupdate FROM market_data_itemregionstat WHERE mapregion_id = %s AND invtype_id = %s" % (data['region'], data['item'])
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print "Error: ", e
        print "SQL: ", sql
    history = curs.fetchone()
    # Delete the old region/item stats from the DB if it exists
    sql = "DELETE FROM market_data_itemregionstat WHERE mapregion_id = %s AND invtype_id = %s" % (data['region'], data['item'])
    curs.execute(sql)
    # Grab all the live orders for this item/region combo
    sql = "SELECT price, is_bid, volume_remaining FROM market_data_orders WHERE mapregion_id = %s AND invtype_id = %s" % (data['region'], data['item'])
    curs.execute(sql)
    for record in curs:
        # Depending on buy/sell status, append to the proper list pricing and volume
        if record[1] == False:
            sellprice.append(record[0])
            sellcount.append(record[2])
        else:
            buyprice.append(record[0])
            buycount.append(record[2])
            
    # process the buy side
    if len(buyprice) > 1:
        top = stats.scoreatpercentile(buyprice, 99)
        bottom = stats.scoreatpercentile(buyprice, 5)
        # mask out the top 1% and bottom 5% of orders so we can try to eliminate the BS
        buy_masked = ma.masked_outside(buyprice, bottom, top)
        tempmask = buy_masked.mask
        buycount_masked = ma.array(buycount, mask=tempmask, fill_value = 0)
        ma.fix_invalid(buy_masked, mask=0)
        ma.fix_invalid(buycount_masked, mask=0)
        buyavg = np.nan_to_num(ma.average(buy_masked, 0, buycount_masked))
        buymean = np.nan_to_num(ma.mean(buy_masked))
        buymedian = np.nan_to_num(ma.median(buy_masked))
        if len(buyprice) < 4:
            buyAvg = np.nan_to_num(ma.average(buyprice))
            buyMean = np.nan_to_num(ma.mean(buyprice))
        buyprice.sort()
        buy = buyprice.pop()
        
    # same processing for sell side as buy side
    if len(sellprice) > 1:
        top = stats.scoreatpercentile(sellprice, 95)
        bottom = stats.scoreatpercentile(sellprice, 1)
        sell_masked = ma.masked_outside(sellprice, bottom, top)
        tempmask = sell_masked.mask
        sellcount_masked = ma.array(sellcount, mask=tempmask, fill_value = 0)
        ma.fix_invalid(sell_masked, mask=0)
        ma.fix_invalid(sellcount_masked, mask=0)
        sellavg = np.nan_to_num(ma.average(sell_masked, 0, sellcount_masked))
        sellmean = np.nan_to_num(ma.mean(sell_masked))
        sellmedian = np.nan_to_num(ma.median(sell_masked))
        if len(sellprice) < 4:
            sellAvg = np.nan_to_num(ma.average(sellprice))
            sellMean = np.nan_to_num(ma.mean(sellprice))
        sellprice.sort()
        sell = sellprice.pop()
    
    # process for history
    if (history is not None) and (history[6] is not None):
        if history[6].date() <> timestamp:
            if (TERM_OUT==True):
                print "--- New date, new insert", data['region'], " / ", data['item'], "(", history[6].date(), " - ", timestamp, ")"
            # dates differ, need to move the data
            sql = "INSERT INTO market_data_itemregionstathistory (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, mapregion_id, invtype_id, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (history[0], history[1], history[2], history[3], history[4], history[5], data['region'], data['item'], history[6])
            try:
                curs.execute(sql)
            except psycopg2.DatabaseError, e:
                print "Error: ", e
                print "SQL: ", sql
        elif (TERM_OUT==True):
            print "/// Timestamps match:", data['region'], " / ", data['item'], "(", history[6].date(), " - ", timestamp, ")"
    else:
        if (TERM_OUT==True):
            print "--- No history, new insert", data['region'], " / ", data['item']
        sql = "INSERT INTO market_data_itemregionstathistory (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, mapregion_id, invtype_id, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, data['region'], data['item'], timestamp)
        try:
            curs.execute(sql)
        except psycopg2.DatabaseError, e:
            print "Error: ", e
            print "SQL: ", sql
        
        
    # insert it into the DB
    sql = "INSERT INTO market_data_itemregionstat (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, mapregion_id, invtype_id, lastupdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, data['region'], data['item'], timestamp)
    #print sql
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print "Error: ", e
        print "SQL: ", sql

if __name__ == '__main__':
    main()

