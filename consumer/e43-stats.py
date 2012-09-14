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

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read(['consumer.conf', 'local_consumer.conf'])
redisdb = config.get('Redis', 'redishost')
dbhost = config.get('Database', 'dbhost')
dbname = config.get('Database', 'dbname')
dbuser = config.get('Database', 'dbuser')
dbpass = config.get('Database', 'dbpass')
dbport = config.get('Database', 'dbport')

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
    
    curs = dbcon.cursor()
    
    sql = "DELETE FROM market_data_itemregionstat WHERE mapregion_id = %s AND invtype_id = %s" % (data['region'], data['item'])
    curs.execute(sql)
    sql = "SELECT price, is_bid, volume_remaining FROM market_data_orders WHERE mapregion_id = %s AND invtype_id = %s" % (data['region'], data['item'])
    curs.execute(sql)
    for record in curs:
        if record[1] == False:
            sellprice.append(record[0])
            sellcount.append(record[2])
        else:
            buyprice.append(record[0])
            buycount.append(record[2])
            
    if len(buyprice) > 1:
        top = stats.scoreatpercentile(buyprice, 99)
        bottom = stats.scoreatpercentile(buyprice, 5)
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
        
    sql = "INSERT INTO market_data_itemregionstat (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, mapregion_id, invtype_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" % (buymean, buyavg, buymedian, sellmean, sellavg, sellmedian, data['region'], data['item'])
    try:
        curs.execute(sql)
    except psycopg2.DatabaseError, e:
        print "Error: ", e
        print "SQL: ", sql

if __name__ == '__main__':
    main()

