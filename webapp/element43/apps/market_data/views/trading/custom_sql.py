from django.db import connection, transaction

def import_markup(local_station_id=60008494, buy_region_id=10000002):
    """
    Returns top 100 markup values above 25% for a given station in comparison to a certain region.
    Defaults
        Buy region: The Forge
        Local station: Amarr VIII (Oris) - Emperor Family Academy
    Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    """
    
    cursor = connection.cursor()
    
    params = [buy_region_id, local_station_id, local_station_id]
    
    query = """SELECT *
            FROM (
                SELECT t.id, t.name, s.foreign_sell, b.local_buy,
                	   ((b.local_buy / s.foreign_sell) - 1) * 100 AS markup
                FROM eve_db_invtype t
                INNER JOIN ( SELECT invtype_id, sellmedian AS foreign_sell 
                			 FROM market_data_itemregionstat 
                			 WHERE mapregion_id = %s) s ON (t.id = s.invtype_id AND foreign_sell > 0)

                INNER JOIN ( SELECT invtype_id, Avg(price) AS local_buy
                			 FROM market_data_orders
                			 WHERE stastation_id = %s
                			 GROUP BY invtype_id ) b ON (t.id = b.invtype_id AND local_buy > 0)

                WHERE t.id IN ( SELECT DISTINCT market_data_orders.invtype_id 
                				FROM market_data_orders
                				WHERE market_data_orders.stastation_id = %s )
            ) q 
            WHERE q.markup > 25
            ORDER BY q.markup DESC
            LIMIT 100;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return cursor.fetchall()