# Utility imports
import datetime
import pytz
from celery.task.schedules import crontab
from celery.task import PeriodicTask, Task
import ast

# Models
from apps.market_data.models import History, OrderHistory


class ProcessHistory(PeriodicTask):

    """
    Post-process history table
    """

    # execute at midnight +1 minute UTC
    run_every = crontab(hour=0, minute=1)
    #run_every = datetime.timedelta(minutes=2)

    def run(self, **kwargs):
        print "BEGIN HISTORY PROCESSING"
        regions = History.objects.order_by('mapregion__id').distinct('mapregion')
        for region in regions.iterator():
            ProcessRegionHistory.delay(region.mapregion)


class ProcessRegionHistory(Task):

    def run(self, region):
        utc = pytz.UTC
        added = 0
        duplicated = 0
        history = History.objects.filter(mapregion=region).order_by('invtype__id')
        print "Starting: %s (r: %s)" % (region, len(history))

        # Create list of items and bluk create them for performance
        bulk_list = []

        # Create timestamp to measure peformance
        start = datetime.datetime.now()

        for message in history.iterator():
            data = ast.literal_eval(message.history_data)

            #print "REGION: %s (i: %s / m: %s)" % (region, message.invtype_id, len(data))
            for k, v in data.iteritems():
                date = utc.localize(datetime.datetime.strptime(k, "%Y-%m-%d %H:%M:%S"))
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
        diff = datetime.datetime.now() - start
        OrderHistory.objects.bulk_create(bulk_list)

        # Prevent division by 0
        if not diff.seconds == 0:
            print "Completed: %s (a: %s / d: %s) at %d items per second." % (region, added, duplicated, ((added + duplicated) / diff.seconds))
        else:
            print "Completed: %s (a: %s / d: %s)" % (region, added, duplicated)
