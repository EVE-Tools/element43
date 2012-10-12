from django.db import connection, transaction

def bid_ask_spread(station_id=60008694):
    """
    Returns top 100 spread items on a given station. 
    This can especially be useful for identifying items worth for station trading if you take the volume into account (high turnover rate).
    Defaults to Jita IV - Moon 4 - Caldari Navy Assembly Plant.
    """
    
    cursor = connection.cursor()
    params = [station_id, station_id]
    
    query = """SELECT *
               FROM (
                    SELECT t.id, t.name, b.max_bid, a.min_ask, 
                           (a.min_ask - b.max_bid) AS spread, 
                           ((a.min_ask / b.max_bid) - 1) * 100 AS spread_percent
                    FROM eve_db_invtype t
                    INNER JOIN ( SELECT invtype_id, Max(price) AS max_bid
                    			 FROM market_data_orders
                    			 WHERE stastation_id = %s AND is_bid = 't' AND is_suspicious = 'f' AND minimum_volume = 1
    							 GROUP BY invtype_id ) b ON (t.id = b.invtype_id AND max_bid > 0)
                    INNER JOIN ( SELECT invtype_id, Min(price) AS min_ask
                    			 FROM market_data_orders
                    			 WHERE stastation_id = %s AND is_bid = 'f' AND is_suspicious = 'f' AND minimum_volume = 1
    							 GROUP BY invtype_id ) a ON (t.id = a.invtype_id AND min_ask > 0)
                ) q 
    			WHERE q.spread > 0
                ORDER BY q.spread DESC
                LIMIT 100;"""
    
    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return cursor.fetchall()

def import_markup(import_station_id=60008494, export_region_id=0, export_system_id=0, export_station_id=60003760):
    """
    Returns top 100 markup values above 0% for a given station in comparison to a certain region, system or station.
    Passing in an export_region will do a region->station comparison.  If 0 is passed in it will do a station->system/station.
    Defaults
        Export region: None
        Export system: None
        Import station: Amarr VIII (Oris) - Emperor Family Academy
        Export station: Jita IV - Moon 4 - Caldari Navy Assembly Plant
    Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    """
    
    cursor = connection.cursor()
    
    if export_region_id:
        params = [export_region_id, import_station_id, import_station_id]
    elif export_system_id:
        params = [export_system_id, import_station_id, import_station_id]
    else:
        params = [export_station_id, import_station_id, import_station_id]
    
    query = """SELECT *
            FROM (
                SELECT t.id, t.name, s.foreign_sell, b.local_buy,
                	   ((b.local_buy / s.foreign_sell) - 1) * 100 AS markup
                FROM eve_db_invtype t
            """
    if export_region_id:
        query += """
                INNER JOIN ( SELECT invtype_id, Min(price) AS foreign_sell
                                        FROM market_data_orders
                                        WHERE mapregion_id = %s AND is_bid = 'f' AND is_suspicious = 'f'
                                        GROUP BY invtype_id ) s ON (t.id = s.invtype_id AND foreign_sell > 0)
                """
    elif export_system_id:
        query += """
                INNER JOIN ( SELECT invtype_id, Min(price) AS foreign_sell
                                        FROM market_data_orders
                                        WHERE mapsolarsystem_id = %s AND is_bid = 'f' AND is_suspicious = 'f'
                                        GROUP BY invtype_id ) s ON (t.id = s.invtype_id AND foreign_sell > 0)
                 """
    else:
        query += """
                INNER JOIN ( SELECT invtype_id, Min(price) AS foreign_sell
                                        FROM market_data_orders
                                        WHERE stastation_id = %s AND is_bid = 'f' AND is_suspicious = 'f'
                                        GROUP BY invtype_id ) s ON (t.id = s.invtype_id AND foreign_sell > 0)
                """
    query += """
                INNER JOIN ( SELECT invtype_id, Max(price) AS local_buy
                			 FROM market_data_orders
                			 WHERE stastation_id = %s AND is_bid = 't' AND is_suspicious = 'f'
                			 GROUP BY invtype_id ) b ON (t.id = b.invtype_id AND local_buy > 0)

                WHERE t.id IN ( SELECT DISTINCT market_data_orders.invtype_id 
                				FROM market_data_orders
                				WHERE market_data_orders.stastation_id = %s )
            ) q 
            WHERE q.markup > 0
            ORDER BY q.markup DESC
            LIMIT 100;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return cursor.fetchall()