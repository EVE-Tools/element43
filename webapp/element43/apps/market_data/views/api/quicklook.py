# numpy processing imports
import numpy as np

# Template and context-related imports
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

# Aggregation
from django.db.models import Min
from django.db.models import Max
from django.db.models import StdDev

# market_data models
from apps.market_data.models import Orders
from apps.market_data.models import OrderHistory
from apps.market_data.models import ItemRegionStat

# utility
import ujson as json

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
                                     is_bid=True).aggregate(Min('price'), Max('price'))
    sellstats = Orders.active.filter(invtype_id=params['typeid'][0],
                                     mapregion_id=params['regionlimit'][0],
                                     is_bid=False).aggregate(Min('price'), Max('price'))
    
    info = []
    info.append(params)
    info.append(stats)
    info.append(buystats)
    info.append(sellstats)
    
    response = json.dumps(info)
    
    return HttpResponse(info, mimetype="application/json")