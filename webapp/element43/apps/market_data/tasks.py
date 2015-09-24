# Utility imports
import datetime
import ast
import pytz

# Util
from datetime import datetime, timedelta

# Celery
from celery.task import PeriodicTask, Task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

# Raw SQL
from django.db import connection

# Models
from apps.market_data.models import History, OrderHistory


logger = get_task_logger(__name__)


class ArchiveOrders(PeriodicTask):

    """
    Archives inactive orders older than a day
    """

    # execute at downtime
    run_every = crontab(hour=11, minute=0)

    def run(self, **kwargs):

        a_day_ago = datetime.now() - timedelta(days=1)

        cursor = connection.cursor()

        logger.warning("Cleaning DB...")

        # Remove duplicate rows which might be a result of an incomplete priror attept
        cursor.execute("""DELETE FROM
                            market_data_archivedorders
                          WHERE
                            ID IN (
                                SELECT
                                    market_data_orders.id
                                FROM
                                    market_data_orders
                                INNER JOIN market_data_archivedorders ON market_data_orders.id = market_data_archivedorders.id
                            );""")

        logger.warning("Moving orders to archive...")

        # Move orders to the archive
        cursor.execute("""INSERT INTO market_data_archivedorders (
                            generated_at,
                            price,
                            volume_remaining,
                            volume_entered,
                            minimum_volume,
                            order_range,
                            ID,
                            is_bid,
                            issue_date,
                            duration,
                            is_suspicious,
                            uploader_ip_hash,
                            mapregion_id,
                            invtype_id,
                            stastation_id,
                            mapsolarsystem_id,
                            is_active
                        ) SELECT
                            generated_at,
                            price,
                            volume_remaining,
                            volume_entered,
                            minimum_volume,
                            order_range,
                            ID,
                            is_bid,
                            issue_date,
                            duration,
                            is_suspicious,
                            uploader_ip_hash,
                            mapregion_id,
                            invtype_id,
                            stastation_id,
                            mapsolarsystem_id,
                            is_active
                        FROM
                            market_data_orders
                        WHERE
                            is_active = 'f'
                        AND generated_at <= \'""" + str(a_day_ago) + "'::TIMESTAMP AT TIME ZONE 'UTC';")

        logger.warning("Done moving orders.")

        logger.warning("Deleting old orders...")

        # Delete moved orders
        cursor.execute("""DELETE FROM
                            market_data_orders
                        WHERE
                            is_active = 'f'
                        AND generated_at <= \'""" + str(a_day_ago) + "'::TIMESTAMP AT TIME ZONE 'UTC';")

        logger.warning("Successfully removed old orders.")


class ProcessHistory(PeriodicTask):

    """
    Post-process history table
    """

    # execute at midnight +1 minute UTC
    run_every = crontab(hour=0, minute=1)
    #run_every = datetime.timedelta(minutes=2)

    def run(self, **kwargs):
        regions = History.objects.order_by('mapregion__id').distinct('mapregion')
        for region in regions.iterator():
            ProcessRegionHistory.delay(region.mapregion)

        logger.warning("Scheduled %d history updates." % len(regions))


class ProcessRegionHistory(Task):

    def run(self, region):
        utc = pytz.UTC
        added = 0
        duplicated = 0
        history = History.objects.filter(mapregion=region).order_by('invtype__id')
        logger.debug("Starting: %s (r: %s)" % (region, len(history)))

        # Create list of items and bluk create them for performance
        bulk_list = []

        # Create timestamp to measure peformance
        start = datetime.now()

        for message in history.iterator():
            data = ast.literal_eval(message.history_data)

            #print "REGION: %s (i: %s / m: %s)" % (region, message.invtype_id, len(data))
            for k, v in data.iteritems():
                date = utc.localize(datetime.strptime(k, "%Y-%m-%d %H:%M:%S"))
                #print "key: %s - date: %s" % (k, date)

                if not OrderHistory.objects.filter(mapregion=region, invtype=message.invtype, date=date).exists():
                    # If datapoint does not exist, append to bulk creation list
                    bulk_list.append(OrderHistory(mapregion=message.mapregion,
                                                  invtype=message.invtype,
                                                  date=date,
                                                  numorders=v[0],
                                                  low=v[1],
                                                  high=v[2],
                                                  mean=v[3],
                                                  quantity=v[4]))
                    added += 1
                else:
                    duplicated += 1

            message.delete()

        # Bulk create objects
        # TODO: with Django 1.5 add batch size to parameter so we don't create ~30k objects per request
        diff = datetime.now() - start
        OrderHistory.objects.bulk_create(bulk_list)

        # Prevent division by 0
        if not diff.seconds == 0:
            logger.warning("Completed: %s (a: %s / d: %s) at %d items per second." % (region, added, duplicated, ((added + duplicated) / diff.seconds)))
        else:
            logger.warning("Completed: %s (a: %s / d: %s)" % (region, added, duplicated))
