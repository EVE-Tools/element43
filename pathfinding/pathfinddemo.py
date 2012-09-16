#!/usr/bin/env python

"""
Preprocess for pathfinding tables
Greg Oberfield - gregoberfield@gmail.com
"""

import psycopg2
import psycopg2.extras
import time
import ConfigParser
import os
import re
import networkx as nx
from hotqueue import HotQueue
import sys

# Load connection params from the configuration file
config = ConfigParser.ConfigParser()
config.read(['processor.conf', 'local_processor.conf'])
dbhost = config.get('Database', 'dbhost')
dbname = config.get('Database', 'dbname')
dbuser = config.get('Database', 'dbuser')
dbpass = config.get('Database', 'dbpass')
dbport = config.get('Database', 'dbport')
redisdb = config.get('Redis', 'redishost')
TERM_OUT = config.get('Consumer', 'term_out')

# list of accessible regions, use this as the base set to identify navigable systems in the DB
region_list = (10000001,10000002,10000003,10000005,10000006,10000007,10000008,10000009,10000010,10000011,10000012,10000013,10000014,10000015,10000016,10000018,10000020,10000021,10000022,10000023,10000025,10000027,10000028,10000067,10000029,10000030,10000031,10000032,10000033,10000034,10000035,10000036,10000037,10000038,10000039,10000040,10000041,10000042,10000043,10000044,10000045,10000046,10000047,10000048,10000049,10000050,10000051,10000052,10000053,10000054,10000055,10000056,10000057,10000058,10000059,10000060,10000061,10000062,10000063,10000064,10000065,10000066,10000068,10000069)

# Connect to PostgreSQL, auto commit.
dbcon = psycopg2.connect("host="+dbhost+" user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport)
dbcon.autocommit = True
# Initialize the global graph for pathfinding
G = nx.Graph()
system_list={}

def main():
    curs = dbcon.cursor()
    sql = "SELECT id, name, security_level FROM eve_db_mapsolarsystem WHERE region_id IN %s"
    curs.execute(sql, [region_list])
    systems = curs.fetchall()
    for system in systems:
        # Add a node for each accessible system
        G.add_node(system[0], name=system[1], seclevel=system[2])
    sql = "SELECT from_solar_system_id, to_solar_system_id FROM eve_db_mapsolarsystemjump WHERE from_region_id IN %s"
    curs.execute(sql, [region_list])
    results = curs.fetchall()
    for row in results:
        # add an edge for each jumpgate
        cost = 1
        if (G.node[row[0]]['seclevel']<0.5) or (G.node[row[1]]['seclevel']<0.5):
            cost = 50
        G.add_edge(row[0], row[1], weight=cost)
    
    print len(results)
    print "Jita neighbors: ", G.neighbors(30000142)
    path = nx.shortest_path(G, source=30000001, target=30000142, weight='weight')
    path_tuple = tuple(path)
    print path
    
    sql = "SELECT name, security_level FROM eve_db_mapsolarsystem WHERE id IN %s"
    curs.execute(sql, [path_tuple])
    result = curs.fetchall()
    output = ""
    for system in result:
        output += " %s (%s) / " % (system[0], system[1])
    print "Path:", output

if __name__ == '__main__':
    main()