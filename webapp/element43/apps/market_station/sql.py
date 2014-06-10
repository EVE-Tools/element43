from django.db import connection
from apps.common.util import dictfetchall


def group_volume(station_id=60008694):

    """
    Returns the total/ask/bid ISK volume by market group in a
    given station in descending order.
    """

    cursor = connection.cursor()
    params = [station_id]

    query = """ SELECT market_group_id,
                    SUM (total) AS group_total,
                    SUM (total_bid) AS group_total_bid,
                    SUM (total_ask) AS group_total_ask
                FROM (
                    SELECT
                        invtype_id,
                        SUM (price * volume_remaining) AS total,
                        SUM (CASE WHEN is_bid = TRUE THEN price * volume_remaining ELSE 0 END) AS total_bid,
                        SUM (CASE WHEN is_bid = FALSE THEN price * volume_remaining ELSE 0 END) AS total_ask
                    FROM
                        market_data_orders
                    WHERE
                        (
                            market_data_orders.is_active = TRUE
                            AND market_data_orders.stastation_id = %s
                            AND market_data_orders.minimum_volume = 1
                        )
                    GROUP BY
                        invtype_id
                    ORDER BY
                        total DESC
                ) AS "total"
                INNER JOIN eve_db_invtype ON (invtype_id = eve_db_invtype. ID)
                GROUP BY
                    market_group_id
                ORDER BY
                    group_total DESC;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return dictfetchall(cursor)


def type_volume(station_id=60008694):

    """
    Returns the total/ask/bid ISK volume by type in a
    given station in descending order.
    """

    cursor = connection.cursor()
    params = [station_id]

    query = """ SELECT
                    invtype_id,
                    SUM (price * volume_remaining) AS total,
                    SUM (CASE WHEN is_bid = TRUE THEN price * volume_remaining ELSE 0 END) AS total_bid,
                    SUM (CASE WHEN is_bid = FALSE THEN price * volume_remaining ELSE 0 END) AS total_ask
                FROM
                    market_data_orders
                WHERE
                    (
                        market_data_orders.is_active = TRUE
                        AND market_data_orders.stastation_id = %s
                        AND market_data_orders.minimum_volume = 1
                    )
                GROUP BY
                    invtype_id
                ORDER BY
                    total DESC;"""

    # Data retrieval operation - no commit required
    cursor.execute(query, params)

    return dictfetchall(cursor)