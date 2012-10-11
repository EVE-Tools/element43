# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count

# eve_db models
from apps.market_data.models import Orders, OrderHistory
from eve_db.models import StaStation
from eve_db.models import MapRegion
from eve_db.models import MapSolarSystem
from eve_db.models import InvType

# Util
import datetime
import ast
from operator import itemgetter

# Helper functions
from apps.market_data.util import group_breadcrumbs
from apps.market_data.sql import import_markup
from django.db.models import Min, Max, Sum

# Caching
from django.views.decorators.cache import cache_page

# Caches this view 1 hour long
@cache_page(60 * 60)
def ranking(request, group = 0):
    """
    This file generates the station ranks based on active orders in the DB
    """
    
    rank_list = Orders.objects.values('stastation__id').annotate(ordercount=Count('id')).order_by('-ordercount')[:50]
    
    for rank in rank_list:
        station = StaStation.objects.get(id = rank['stastation__id'])
        rank.update({'system': station.solar_system, 'name': station.name, 'region': station.region, 'id': station.id})
    
    generated_at = datetime.datetime.now()
    rcontext = RequestContext(request, {'rank_list': rank_list, 'generated_at': generated_at})

    return render_to_response('trading/station/ranking.haml', rcontext)
    
def import_tool(request, station_id = 60003760):
    """
    Generates a list like http://goonmetrics.com/importing/
    """
    
    jita = 60003760
    
    # Get station object - default to CNAP if something goes wrong
    try:
        station = StaStation.objects.get(id = station_id)
    except:
        station_id = jita
        station = StaStation.objects.get(id = station_id)
    
    # Compare to The Forge
    # Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    markup = import_markup(station_id, 0, jita)
    
    # Get history data
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = []
    
    for point in markup:
        # Make list from tuple ans add weekly volume
        # Mapping: [invTyeID, invTypeName, foreign_sell, local_buy, markup, weekly_volume, (+potential profit)]
        new_data = [point[0], point[1], point[2], point[3], point[4], OrderHistory.objects.filter(mapregion_id = station.region.id, invtype_id = point[0], date__gte = last_week).aggregate(Sum("quantity"))['quantity__sum']]
        
        # Calculate potential profit ((foreign_sell - local_buy) * weekly_volume)
        if new_data[5] != None:
            new_data.append((new_data[3] - new_data[2]) * new_data[5])
            data.append(new_data)
    data.sort(key=itemgetter(6), reverse=True)
    
    rcontext = RequestContext(request, {'station':station, 'markup':data})

    return render_to_response('trading/station/station.haml', rcontext)