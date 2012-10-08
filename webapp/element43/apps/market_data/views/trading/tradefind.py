# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count

# eve_db models
from apps.market_data.models import Orders
from eve_db.models import StaStation
from eve_db.models import MapRegion
from eve_db.models import MapSolarSystem
from eve_db.models import InvType

# Helper functions
from apps.market_data.util import group_breadcrumbs

def tradefind(request, source, target):
    if (source >= 10000000) and (source < 20000000):
        source_type = 'region'
    else:
        source_type = 'system'
        
    if (target >= 10000000) and (target < 20000000):
        target_type = 'region'
    else:
        target_type = 'system'
        
    if source=='region':
        tradeorders = Orders.objects.values('')
        
    #rcontext = RequestContext(request, {'rank_list': rank_list, 'generated_at': generated_at})

    #return render_to_response('trading/station/ranking.haml', rcontext)
    return HttpResponse(trade_list)