from django.db import connection

from apps.common.util import dictfetchall


def find_trades(start_id=60008694, destination_id=10000002):

    """
    Returns inter-region trade opportunities.
    """

    cursor = connection.cursor()
    params = [destination_id, start_id, start_id]

    query = """SELECT *
                FROM (
                    SELECT t.id, t.name, t.volume, b.local_ask, a.foreign_bid,
                           ((a.foreign_bid / b.local_ask) - 1) * 100 AS markup
                    FROM eve_db_invtype t
                        INNER JOIN (SELECT invtype_id, buyavg AS foreign_bid
                                    FROM market_data_itemregionstat
                                    WHERE mapregion_id = %s AND lastupdate > current_date - interval '3 days'
                                    ) a ON (t.id = a.invtype_id AND foreign_bid > 0)
                        INNER JOIN (SELECT invtype_id, sellavg AS local_ask
                                    FROM market_data_itemregionstat
                                    WHERE mapregion_id = %s AND lastupdate > current_date - interval '3 days'
                                    ) b ON (t.id = b.invtype_id AND local_ask > 0)
                    WHERE t.id IN (SELECT market_data_itemregionstat.invtype_id
                                   FROM market_data_itemregionstat
                                   WHERE market_data_itemregionstat.mapregion_id = %s)
                ) q
                WHERE q.markup > 0
                ORDER BY q.markup DESC
                LIMIT 50;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return dictfetchall(cursor)