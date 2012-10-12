# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.http import HttpResponse

# eve_db models
from apps.market_data.models import Orders, OrderHistory
from eve_db.models import StaStation
from eve_db.models import MapRegion
from eve_db.models import MapSolarSystem
from eve_db.models import InvType

# JSON for the live search
from django.utils import simplejson

# Util
import datetime
import pytz
import ast
from operator import itemgetter

# Helper functions
from apps.market_data.util import group_breadcrumbs
from apps.market_data.sql import bid_ask_spread, import_markup
from django.db.models import Min, Max, Sum

# Caching
from django.views.decorators.cache import cache_page

def live_search(request):

    """
    This adds a basic live search view to element43.
    The names in the invTypes table are searched with a case insensitive LIKE query and the result is returned as a JSON array of matching names.
    """
    
    if request.GET.get('query'):
        query = request.GET.get('query')
    else:
        query = ""
    
    # Prepare lists
    names = []
    ids = []
    
    # Default to empty array
    json = "{query:'" + query + "', suggestions:[], data:[]}"
    
    # Only if the string is longer than 2 characters start looking in the DB
    if len(query) > 2:
        
        # Load system objects matching the name
        systems = MapSolarSystem.objects.filter(name__icontains = query)
        
        for system in systems:
            names.append(system.name)
            ids.append('system_' + str(system.id))
            
        # Load regions
        regions = MapRegion.objects.filter(name__icontains = query)
        
        for region in regions:
            names.append(region.name)
            ids.append('region_' + str(region.id))
        
        # Add additional data for Ajax AutoComplete
        json = {'query': query, 'suggestions': names, 'data': ids}
        
        # Turn names into JSON
        json = simplejson.dumps(json)
    
    # Return JSON without using any template
    return HttpResponse(json, mimetype = 'application/json')

def station(request, station_id = 60003760):
    """
    Shows station info.
    Defaults to Jita CNAP.
    """
    jita = 60003760
    
    # Get station object - default to CNAP if something goes wrong
    try:
        station = StaStation.objects.get(id = station_id)
    except:
        station_id = jita
        station = StaStation.objects.get(id = station_id)
        
    # Get Bid/Ask Spread
    # Mapping: (invTyeID, invTypeName, max_bid, min_ask, spread, spread_percent)
    spread = bid_ask_spread(station_id)
    
    # Get history data
    last_week = pytz.utc.localize(datetime.datetime.utcnow() - datetime.timedelta(days=7))
    data = []
    
    for point in spread:
        # Make list from tuple ans add weekly volume
        # Mapping: [invTyeID, invTypeName, local_buy, local_buy_qty_within_1%, foreign_sell, foreign_sell_qty_within_1%, spread, spread %, weekly_volume, (+potential profit)]
        new_data = [point[0],
                    point[1],
                    point[2],
                    Orders.objects.filter(stastation_id = station.id, invtype_id = point[0], is_bid=True, price__lte = (point[2]+(point[2]*0.01))).aggregate(Sum("volume_remaining"))['volume_remaining__sum'],
                    point[3],
                    Orders.objects.filter(stastation_id = station.id, invtype_id = point[0], is_bid=False, price__gte = (point[3]-(point[3]*0.01))).aggregate(Sum("volume_remaining"))['volume_remaining__sum'],
                    point[4],
                    point[5],
                    OrderHistory.objects.filter(mapregion_id = station.region.id, invtype_id = point[0], date__gte = last_week).aggregate(Sum("quantity"))['quantity__sum']]
        
        # Calculate potential daily profit ((max_bid - min_ask) * weekly_volume) / 7
        # We're using a week's worth of data to eliminate fluctuations
        if new_data[8] != None:
            new_data.append((((point[3] - point[2]) * new_data[8]) / 7))
            data.append(new_data)
            
    data.sort(key=itemgetter(9), reverse=True)
    rcontext = RequestContext(request, {'station':station, 'spread':data})
    
    return render_to_response('trading/station/station.haml', rcontext)
    

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
    # the station id of Jita IV/4
    jita = 60003760
    
    # Get station object - default to CNAP if something goes wrong
    try:
        station = StaStation.objects.get(id = station_id)
    except:
        station_id = jita
        station = StaStation.objects.get(id = station_id)
    
    # Compare to The Forge
    # Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    markup = import_markup(station_id, 0, 0, jita)
    
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

    return render_to_response('trading/station/import.haml', rcontext)
    
def import_system(request, station_id = 60003760, system_id = 30000142):
    """
    Generates a list like http://goonmetrics.com/importing/
    """

    system = MapSolarSystem.objects.get(id = system_id)
    
    # Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    markup = import_markup(station_id, 0, system_id, 0)
    
    # Get history data
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = []
    
    for point in markup:
        # Make list from tuple ans add weekly volume
        # Mapping: [invTyeID, invTypeName, foreign_sell, local_buy, markup, weekly_volume, (+potential profit)]
        new_data = [point[0],
                    point[1],
                    point[2],
                    point[3],
                    point[4],
                    OrderHistory.objects.filter(mapregion_id = system.region.id, invtype_id = point[0], date__gte = last_week).aggregate(Sum("quantity"))['quantity__sum'],
                    Orders.objects.filter(mapsystem_id = station.system.id, invtype_id = point[0], is_bid=True, price__lte = (point[2]+(point[2]*0.01))).aggregate(Sum("volume_remaining"))['volume_remaining__sum'],
                    Orders.objects.filter(mapsystem_id = station.system.id, invtype_id = point[0], is_bid=False, price__gte = (point[3]-(point[3]*0.01))).aggregate(Sum("volume_remaining"))['volume_remaining__sum']]
        
        # Calculate potential profit ((foreign_sell - local_buy) * weekly_volume)
        if new_data[5] != None:
            new_data.append((new_data[3] - new_data[2]) * new_data[5])
            data.append(new_data)
    data.sort(key=itemgetter(8), reverse=True)    
    rcontext = RequestContext(request, {'system':system, 'markup':data})

    return render_to_response('trading/station/_import_system.haml', rcontext)

    
def import_region(request, station_id = 60003760, region_id = 10000002):
    """
    Generates a list like http://goonmetrics.com/importing/
    """

    region = MapRegion.objects.get(id = region_id)
    
    # Mapping: (invTyeID, invTypeName, foreign_sell, local_buy, markup, invTyeID)
    markup = import_markup(station_id, region_id, 0, 0)
    
    # Get history data
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = []
    
    for point in markup:
        # Make list from tuple ans add weekly volume
        # Mapping: [invTyeID, invTypeName, foreign_sell, local_buy, markup, weekly_volume, (+potential profit)]
        new_data = [point[0], point[1], point[2], point[3], point[4], OrderHistory.objects.filter(mapregion_id = region.id, invtype_id = point[0], date__gte = last_week).aggregate(Sum("quantity"))['quantity__sum']]
        
        # Calculate potential profit ((foreign_sell - local_buy) * weekly_volume)
        if new_data[5] != None:
            new_data.append((new_data[3] - new_data[2]) * new_data[5])
            data.append(new_data)
    data.sort(key=itemgetter(6), reverse=True)
    
    rcontext = RequestContext(request, {'region':region, 'markup':data})

    return render_to_response('trading/station/_import_region.haml', rcontext)
