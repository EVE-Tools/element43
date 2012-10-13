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
        print "STARTING: %s (r: %s)" % (region, len(history))
        for message in history.iterator():
            data = ast.literal_eval(message.history_data)
            #print "REGION: %s (i: %s / m: %s)" % (region, message.invtype_id, len(data))
            for k, v in data.iteritems():
                date = utc.localize(datetime.datetime.strptime(k, "%Y-%m-%d %H:%M:%S"))
                #print "key: %s - date: %s" % (k, date)
                if not OrderHistory.objects.filter(mapregion=region, invtype=message.invtype, date=date).exists():
                    new_history = OrderHistory(mapregion=message.mapregion,
                                               invtype=message.invtype,
                                               date=date,
                                               numorders=v[0],
                                               low=v[1],
                                               high=v[2],
                                               mean=v[3],
                                               quantity=v[4])
                    new_history.save()
                    added += 1
                else:
                    duplicated += 1
            message.delete()
        print "Completed: %s (a: %s / d: %s)" % (region, added, duplicated)
