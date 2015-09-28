# Template and context-related imports
from django.http import HttpResponse

# Aggregation
from django.db.models import Min
from django.db.models import Max

# market_data models
from apps.market_data.models import Orders
from apps.market_data.models import ItemRegionStat

# utility
import json

def quicklook(request):
    """
    This is the JSON response object for the API, not E-C safe

    TODO: multiple regions submitted, multiple typeIDs, better error handling
    """

    params = {}
    # parse GET parameters and put them into a dict to make life easier
    for key in request.GET.iterkeys():
        params[key]=request.GET.getlist(key)

    stats = ItemRegionStat.objects.filter(invtype_id=params['typeid'][0],
                                          mapregion_id=params['regionlimit'][0])
    buystats = Orders.active.filter(invtype_id=params['typeid'][0],
                                     mapregion_id=params['regionlimit'][0],
                                     is_bid=True).aggregate(minprice=Min('price'), maxprice=Max('price'))
    sellstats = Orders.active.filter(invtype_id=params['typeid'][0],
                                     mapregion_id=params['regionlimit'][0],
                                     is_bid=False).aggregate(minprice=Min('price'), maxprice=Max('price'))

    info = {}
    info['invtype']=int(params['typeid'][0])
    info['region']=int(params['regionlimit'][0])

    buy = {}
    sell = {}
    for stat in stats:
        buy['mean'] = stat.buymean
        buy['average'] = stat.buyavg
        buy['median'] = stat.buymedian
        buy['std_dev'] = stat.buy_std_dev
        buy['95percentile'] = stat.buy_95_percentile
        buy['volume'] = stat.buyvolume
        sell['mean'] = stat.sellmean
        sell['average'] = stat.sellavg
        sell['median'] = stat.sellmedian
        sell['std_dev'] = stat.sell_std_dev
        sell['95percentile'] = stat.sell_95_percentile
        sell['volume'] = stat.sellvolume

    buy['min'] = buystats['minprice']
    buy['max'] = buystats['maxprice']

    sell['min'] = sellstats['minprice']
    sell['max'] = sellstats['maxprice']

    api_json = json.dumps({'info':info,
                           'buy_stats':buy,
                           'sell_stats':sell})

    return HttpResponse(api_json, content_type="application/json")
