from django.db import connection

from apps.common.util import dictfetchall


def bid_ask_spread(station_id=60008694, region_id=10000002, market_group_id=1413):

    """
    Returns top 100 spread items on a given station.
    This can especially be useful for identifying items worth for station trading if you take the volume into account.
    Defaults to Jita IV - Moon 4 - Caldari Navy Assembly Plant.
    """

    cursor = connection.cursor()
    params = [market_group_id, station_id, station_id, region_id]

    query = """SELECT id, name, min_ask, max_bid, spread, spread_percent, weekly_volume,
                     ((min_ask - max_bid) * weekly_volume / 7) AS potential_daily_profit
               FROM (
                    SELECT t.id, t.name, b.max_bid, a.min_ask,
                           (a.min_ask - b.max_bid) AS spread,
                           ((a.min_ask / b.max_bid) - 1) * 100 AS spread_percent
                    FROM ( SELECT id, name
                           FROM eve_db_invtype z
                           WHERE market_group_id = %s AND is_published = 't') t

                    INNER JOIN ( SELECT invtype_id, Max(price) AS max_bid
                                 FROM market_data_orders
                                 WHERE stastation_id = %s AND is_bid = 't' AND is_suspicious = 'f' AND minimum_volume = 1
                                 GROUP BY invtype_id ) b ON (t.id = b.invtype_id AND max_bid > 0)
                    INNER JOIN ( SELECT invtype_id, Min(price) AS min_ask
                                 FROM market_data_orders
                                 WHERE stastation_id = %s AND is_bid = 'f' AND is_suspicious = 'f' AND minimum_volume = 1
                                 GROUP BY invtype_id ) a ON (t.id = a.invtype_id AND min_ask > 0)
                ) q
                INNER JOIN ( SELECT invtype_id, Sum(quantity) AS weekly_volume
                             FROM market_data_orderhistory
                             WHERE mapregion_id = %s AND date >= current_date - interval '7 days'
                             GROUP BY invtype_id ) v ON (q.id = invtype_id AND weekly_volume > 0)
                ORDER BY potential_daily_profit DESC;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return dictfetchall(cursor)


def import_markup(import_station_id=60008494, export_region_id=0, export_system_id=0, export_station_id=60003760):

    """
    Returns top 100 markup values above 0% for a given station in comparison to a certain region, system or station.
    Passing in an export_region will do a region->station comparison.
    If 0 is passed in it will do a station->system/station.

    Defaults
        Export region: None
        Export system: None
        Import station: Amarr VIII (Oris) - Emperor Family Academy
        Export station: Jita IV - Moon 4 - Caldari Navy Assembly Plant

    Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    """

    cursor = connection.cursor()

    # Build params
    if export_region_id:
        params = [export_region_id, import_station_id, import_station_id]
    elif export_system_id:
        params = [export_system_id, import_station_id, import_station_id]
    else:
        params = [export_station_id, import_station_id, import_station_id]

    query = """SELECT *
            FROM (
                SELECT t.id, t.name, a.foreign_ask, b.local_bid,
                       ((b.local_bid / a.foreign_ask) - 1) * 100 AS markup
                FROM eve_db_invtype t
                INNER JOIN (SELECT invtype_id, Min(price) AS foreign_ask
                            FROM market_data_orders """

    # Build query based on params
    if export_region_id:
        query += "WHERE mapregion_id = %s "
    elif export_system_id:
        query += "WHERE mapsolarsystem_id = %s "
    else:
        query += "WHERE stastation_id = %s "

    query += """ AND is_bid = 'f' AND is_suspicious = 'f'
                GROUP BY invtype_id ) a ON (t.id = a.invtype_id AND foreign_ask > 0)
            INNER JOIN (SELECT invtype_id, Max(price) AS local_bid
                        FROM market_data_orders
                        WHERE stastation_id = %s AND is_bid = 't' AND is_suspicious = 'f'
                        GROUP BY invtype_id ) b ON (t.id = b.invtype_id AND local_bid > 0)

            WHERE t.id IN (SELECT DISTINCT market_data_orders.invtype_id
                           FROM market_data_orders
                           WHERE market_data_orders.stastation_id = %s )
            ) q
            WHERE q.markup > 0
            ORDER BY q.markup DESC
            LIMIT 100;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return dictfetchall(cursor)
