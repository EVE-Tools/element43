# Parsing
import time

# Util
from datetime import datetime, timedelta

# Django Imports
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

# JSON for the history API
import json

# market_data models
from apps.market_data.models import OrderHistory

# Calculate cache time for history JSON. The task for refreshing history messages is fired at 00:01 UTC,
# so it should be finished by 03:00UTC. That's when the cache should expire.


@cache_page(((datetime.utcnow() + timedelta(days=1)).replace(hour=3,
                                                             minute=0,
                                                             second=0,
                                                             microsecond=0) - datetime.utcnow()).seconds)
def history_json(request, region_id=10000002, type_id=34):

    """
    Returns a set of history data in JSON format. Defaults to Tritanium in The Forge.
    """

    # Prepare lists
    ohlc_data = []

    # If we do not have any data for this region, return an empty array
    # Load history and parse data (unsorted)
    data = OrderHistory.objects.filter(mapregion=region_id, invtype=type_id).order_by('date')

    last_mean = 0

    if len(data):
        last_mean = data[0].mean

    # Convert to Highstocks compatible timestamp first
    for point in data:
        ohlc_data.append(
            [int(time.mktime(point.date.timetuple())) * 1000, last_mean, point.high, point.low, point.mean, point.quantity])
        last_mean = point.mean

    serialized = json.dumps(ohlc_data)

    # Return JSON without using any template
    return HttpResponse(serialized, content_type='application/json')


@cache_page(((datetime.utcnow() + timedelta(days=1)).replace(hour=3,
                                                             minute=0,
                                                             second=0,
                                                             microsecond=0) - datetime.utcnow()).seconds)
def history_compare_json(request, type_id=34):

    """
    Returns a set of history data in JSON format. Defaults to Tritanium in The Forge.
    """

    region_ids = [10000002, 10000043, 10000032, 10000030]

    # Prepare lists
    data_dict = {}

    # If we do not have any data for this region, return an empty array
    for region in region_ids:
        data = OrderHistory.objects.filter(mapregion=region, invtype=type_id).order_by('date')
        graph = []

        for point in data:
            graph.append([int(time.mktime(point.date.timetuple())) * 1000, point.mean])

        if graph:
            data_dict[region] = graph

    # If data is empty, return empty list instead of empty dict so the graph does not get rendered
    if not data_dict:
        data_dict = []

    serialized = json.dumps(data_dict)

    # Return JSON without using any template
    return HttpResponse(serialized, content_type='application/json')
