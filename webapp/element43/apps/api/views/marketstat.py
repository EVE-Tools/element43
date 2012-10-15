# numpy processing imports
import numpy as np

# Template and context-related imports
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

# Aggregation
from django.db.models import Sum
from django.db.models import Min

# market_data models
from apps.market_data.models import Orders
from apps.market_data.models import OrderHistory
from apps.market_data.models import ItemRegionStat

def legacy_marketstat(request):
    """
    This will match the Eve-central api for legacy reasons
    
    TODO: multiple regions submitted, multiple typeIDs, better error handling
    """
    
    params = {}
    # parse GET parameters and put them into a dict to make life easier
    for key in request.GET.iterkeys():
        params[key]=values.GET.getlist(key)
    
    