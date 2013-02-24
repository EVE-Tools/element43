# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# Aggregation
from django.db.models import Min
from django.db.models import Max
from django.db.models import Sum

# market_data models
from apps.market_data.models import Orders
from apps.market_data.models import OrderHistory
from apps.market_data.models import ItemRegionStat

# utility
import pytz
import datetime

def legacy_marketstat(request):
    """
    This will match the Eve-central api for legacy reasons

    TODO: multiple regions submitted, multiple typeIDs, better error handling
    """

    params = {}
    mapregion = 10000002
    result_info = []
    # parse GET parameters and put them into a dict to make life easier
    for key in request.GET.iterkeys():
        params[key]=request.GET.getlist(key)

    try:
        mapregion = int(params['regionlimit'][0])
    except:
        mapregion = 10000002

    for item in params['typeid']:
        stats = ItemRegionStat.objects.get(invtype_id=item,
                                              mapregion_id=mapregion)
        buystats = Orders.active.filter(invtype_id=item,
                                         mapregion_id=mapregion,
                                         is_bid=True).aggregate(Min('price'), Max('price'))
        sellstats = Orders.active.filter(invtype_id=item,
                                         mapregion_id=mapregion,
                                         is_bid=False).aggregate(Min('price'), Max('price'))
        result_info.append({'invtype':item, 'stats':stats, 'buystats':buystats, 'sellstats':sellstats})



    rcontext = RequestContext(request, {'params':params,
                                        'result_info':result_info})

    return render_to_response('api/legacy_marketstat.haml', rcontext, mimetype="text/xml")

def marketstat(request):
    """
    This is our own e43 api export that provides more data than other sites

    TODO: multiple regions submitted, multiple typeIDs, better error handling
    """

    params = {}
    mapregion = 10000002
    result_info = []

    # Get last week for history query
    last_week = pytz.utc.localize(
        datetime.datetime.utcnow() - datetime.timedelta(days=7))

    # parse GET parameters and put them into a dict to make life easier
    for key in request.GET.iterkeys():
        params[key]=request.GET.getlist(key)

    try:
        mapregion = int(params['regionlimit'][0])
    except:
        mapregion = 10000002

    for item in params['typeid']:
        stats = ItemRegionStat.objects.get(invtype_id=item,
                                              mapregion_id=mapregion)
        buystats = Orders.active.filter(invtype_id=item,
                                         mapregion_id=mapregion,
                                         is_bid=True).aggregate(Min('price'), Max('price'))
        sellstats = Orders.active.filter(invtype_id=item,
                                         mapregion_id=mapregion,
                                         is_bid=False).aggregate(Min('price'), Max('price'))
        qty = OrderHistory.objects.filter(mapregion_id=mapregion,
                                    invtype_id=item,
                                    date__gte=last_week).aggregate(Sum("quantity"))['quantity__sum']
        result_info.append({'invtype':item, 'qty':qty, 'stats':stats, 'buystats':buystats, 'sellstats':sellstats})



    rcontext = RequestContext(request, {'params':params,
                                        'result_info':result_info})

    return render_to_response('api/marketstat.haml', rcontext, mimetype="text/xml")