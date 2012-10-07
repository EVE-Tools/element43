# Template and context-related imports
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

# Aggregation
from django.db.models import Sum
from django.db.models import Avg

# market_data models
from apps.market_data.models import Orders
from apps.market_data.models import OrderHistory
from apps.market_data.models import ItemRegionStat
from apps.market_data.models import History

# JSON for the history API
from django.utils import simplejson

# Parsing
import ast
import time

# Util
from datetime import datetime, timedelta

# eve_db models
from eve_db.models import InvType
from eve_db.models import InvTypeMaterial
from eve_db.models import MapRegion
from eve_db.models import MapSolarSystem

# numpy processing imports
import numpy as np

# Helper functions
from apps.market_data.util import group_breadcrumbs

def history_json(request, region_id = 10000002, type_id = 34):
    
    """
    Returns a set of history data in JSON format. Defaults to Tritanium in The Forge.
    """
        
    # Prepare lists
    ohlc_data = []
    ohlc_list = []
        
    # If we do not have any data for this region, return an empty array
    # Load history and parse data (unsorted)
    data = OrderHistory.objects.filter(mapregion = region_id, invtype = type_id).order_by('date')
    
    last_mean = 0
    
    if len(data):
        last_mean = data[0].mean
        
    # Convert to Highstocks compatible timestamp first
    for point in data:
        ohlc_data.append([int(time.mktime(point.date.timetuple())) * 1000, last_mean, point.high, point.low, point.mean, point.quantity])
        last_mean = point.mean
        
    json = simplejson.dumps(ohlc_data)
        
    # Return JSON without using any template
    return HttpResponse(json, mimetype = 'application/json')
        
def history_compare_json(request, type_id = 34):
    
    """
    Returns a set of history data in JSON format. Defaults to Tritanium in The Forge.
    """
    
    region_ids = [10000002, 10000043, 10000032, 10000030]
        
    # Prepare lists
    data_dict = {}
        
    # If we do not have any data for this region, return an empty array
    for region in region_ids:
        data = OrderHistory.objects.filter(mapregion = region, invtype = type_id).order_by('date')
        graph = []
        
        for point in data:
            graph.append([int(time.mktime(point.date.timetuple())) * 1000, point.mean])
        
        data_dict[region] = graph
        
    json = simplejson.dumps(data_dict)
        
    # Return JSON without using any template
    return HttpResponse(json, mimetype = 'application/json')

def quicklook_region(request, region_id = 10000002, type_id = 34):
    """
    Generates system level overview for a specific type.
    Defaults to tritanium & the forge.
    """
    
    # Get the item type
    type_object = InvType.objects.get(id = type_id)

    # Get list of materials to build
    materials = InvTypeMaterial.objects.values('material_type__name', 'quantity', 'material_type__id').filter(type=type_id)
    totalprice = 0
    for material in materials:
        # Get jita pricing
        stat_object = ItemRegionStat()
        try:
            stat_object = ItemRegionStat.objects.get(invtype_id__exact=material['material_type__id'], mapregion_id__exact=10000002)
        except:
            stat_object.sellmedian = 0
        material['price']=stat_object.sellmedian
        material['total']=stat_object.sellmedian*material['quantity']
        totalprice += material['total']

    # Get the region type
    region_object = MapRegion.objects.get(id = region_id)

    #
    # Orders
    #
    
    # Fetch all buy/sell orders from DB
    buy_orders = Orders.objects.filter(invtype = type_id, is_bid = True, mapregion_id = region_id).order_by('-price')
    sell_orders = Orders.objects.filter(invtype = type_id, is_bid = False, mapregion_id = region_id).order_by('price')
    
    orders = []
    orders += buy_orders
    orders += sell_orders
    
    systems = []
    for order in orders:
        if not order.mapsolarsystem_id in systems:
            systems.append(order.mapsolarsystem_id)
            
    # Gather system-based data for this type      
    system_data = []
    for system in systems:
        temp_data = []
        
        system_ask_prices = np.array([order.price for order in buy_orders if order.mapsolarsystem_id == system])
        system_bid_prices = np.array([order.price for order in sell_orders if order.mapsolarsystem_id == system])
        
        # Order of array entries: Name, Bid/Ask(Low, High, Average, Median, Standard Deviation, Lots, Volume)
        temp_data.append(MapSolarSystem.objects.get(id=system).name)
        
        if len(system_ask_prices) > 0:
                # Ask values calculated via numpy
                temp_data.append(np.min(system_ask_prices))
                temp_data.append(np.max(system_ask_prices))
                temp_data.append(round(np.average(system_ask_prices),2))
                temp_data.append(np.median(system_ask_prices))
                temp_data.append(round(np.std(system_ask_prices),2))
                temp_data.append(len(system_ask_prices))
                temp_data.append(Orders.objects.filter(mapsolarsystem_id = system, invtype = type_id, is_bid = False).aggregate(Sum('volume_remaining'))['volume_remaining__sum'])
        else:
                # Else there are no orders in this system -> add a bunch of 0s
                temp_data.extend([0,0,0,0,0,0,0])
        
        if len(system_bid_prices) > 0:
                # Bid values calculated via numpy
                temp_data.append(np.min(system_bid_prices))
                temp_data.append(np.max(system_bid_prices))
                temp_data.append(round(np.average(system_bid_prices),2))
                temp_data.append(np.median(system_bid_prices))
                temp_data.append(round(np.std(system_bid_prices),2))
                temp_data.append(len(system_bid_prices))
                temp_data.append(Orders.objects.filter(mapsolarsystem_id = system, invtype = type_id, is_bid = True).aggregate(Sum('volume_remaining'))['volume_remaining__sum'])
        else:
                # Else there are no orders in this system -> add a bunch of 0s
                temp_data.extend([0,0,0,0,0,0,0])
                
        # Append temp_data to system_data
        system_data.append(temp_data)
        # Sort alphabetically by system name
        system_data = sorted(system_data, key=lambda system: system[0])

    breadcrumbs = group_breadcrumbs(type_object.market_group_id)
    # Use all orders for quicklook and add the system_data to the context
    # We shouldn't need to limit the amount of orders displayed here as they all are in the same region
    rcontext = RequestContext(request, {'IMAGE_SERVER':settings.IMAGE_SERVER, 'region':region_object, 'type':type_object, 'materials':materials, 'totalprice':totalprice, 'buy_orders':buy_orders, 'sell_orders':sell_orders, 'systems':system_data, 'breadcrumbs':breadcrumbs})
    
    return render_to_response('market/quicklook/quicklook_region.haml', rcontext)

def quicklook(request, type_id = 34):
        
    """
    Generates a market overview for a certain type. Defaults to tritanium.
    """
    
    # Get the item type
    type_object = InvType.objects.get(id = type_id)
    
    # Add regions
    region_ids = [10000002, 10000043, 10000032, 10000030]
    region_names = []
        
    for region in region_ids:
        region_names.append(MapRegion.objects.get(id = region).name)
    
    # Get requested type
    type_object = InvType.objects.get(id = type_id)
    
    # Get list of materials to build
    materials = InvTypeMaterial.objects.values('material_type__name', 'quantity', 'material_type__id').filter(type=type_id)
    totalprice = 0
    for material in materials:
        # Get jita pricing
        stat_object = ItemRegionStat()
        try:
            stat_object = ItemRegionStat.objects.get(invtype_id__exact=material['material_type__id'], mapregion_id__exact=10000002)
        except:
            stat_object.sellmedian = 0
        material['price']=stat_object.sellmedian
        material['total']=stat_object.sellmedian*material['quantity']
        totalprice += material['total']
    
    # Fetch all buy/sell orders from DB
    buy_orders = Orders.objects.filter(invtype = type_id, is_bid = True).order_by('-price')
    sell_orders = Orders.objects.filter(invtype = type_id, is_bid = False).order_by('price')
    
    # Make list with all orders
    orders = []
    orders += buy_orders
    orders += sell_orders
    
    # Get region IDs of regions with orders for this type
    regions = []
    for order in orders:
        if not order.mapregion_id in regions:
            regions.append(order.mapregion_id)
    
    # Gather region-based data for this type
    region_data = []
    for region in regions:
        # Temporary array for this region - will later be appended to region_data
        temp_data = []
    
        # Get all the prices of this region into a numpy array for processing later on
        region_ask_prices = np.array([order.price for order in buy_orders if order.mapregion_id == region])
        region_bid_prices = np.array([order.price for order in sell_orders if order.mapregion_id == region])
        
        # Order of array entries: Name, Bid/Ask(Low, High, Average, Median, Standard Deviation, Lots, Volume, region id)
        temp_data.append(MapRegion.objects.get(id=region).name)
        
        if len(region_ask_prices) > 0:
            # Ask values calculated via numpy
            temp_data.append(np.min(region_ask_prices))
            temp_data.append(np.max(region_ask_prices))
            temp_data.append(round(np.average(region_ask_prices),2))
            temp_data.append(np.median(region_ask_prices))
            temp_data.append(round(np.std(region_ask_prices),2))
            temp_data.append(len(region_ask_prices))
            temp_data.append(Orders.objects.filter(mapregion_id = region, invtype = type_id, is_bid = False).aggregate(Sum('volume_remaining'))['volume_remaining__sum'])
            temp_data.append(region)
        else:
            # Else there are no orders in this region -> add a bunch of 0s
            temp_data.extend([0,0,0,0,0,0,0])
            temp_data.append(region)
        
        if len(region_bid_prices) > 0:
            # Bid values calculated via numpy
            temp_data.append(np.min(region_bid_prices))
            temp_data.append(np.max(region_bid_prices))
            temp_data.append(round(np.average(region_bid_prices),2))
            temp_data.append(np.median(region_bid_prices))
            temp_data.append(round(np.std(region_bid_prices),2))
            temp_data.append(len(region_bid_prices))
            temp_data.append(Orders.objects.filter(mapregion_id = region, invtype = type_id, is_bid = True).aggregate(Sum('volume_remaining'))['volume_remaining__sum'])
            temp_data.append(region)
        else:
            # Else there are no orders in this region -> add a bunch of 0s
            temp_data.extend([0,0,0,0,0,0,0])
            temp_data.append(region)
            
        # Append temp_data to region_data
        region_data.append(temp_data)
        # Sort alphabetically by region name
        region_data = sorted(region_data, key=lambda region: region[0])
    
    breadcrumbs = group_breadcrumbs(type_object.market_group_id)
    # Use the 50 'best' orders for quicklook and add the region_data to the context
    rcontext = RequestContext(request, {'IMAGE_SERVER':settings.IMAGE_SERVER, 'type':type_object, 'region_ids':region_ids, 'region_names':simplejson.dumps(region_names), 'materials':materials, 'totalprice':totalprice, 'buy_orders':buy_orders[:50], 'sell_orders':sell_orders[:50], 'regions':region_data, 'breadcrumbs':breadcrumbs})
    
    return render_to_response('market/quicklook/quicklook.haml', rcontext)
    
def quicklook_ask_filter(request, type_id = 34, min_sec = 0, max_age = 8):
    """
    Returns quicklook partial for filtering
    """
    
    min_sec = float(min_sec) / 10
    if min_sec == 0:
        min_sec = -10
    
    filter_time = datetime.now() - timedelta(hours = int(max_age))
    
    # Fetch all sell orders from DB
    sell_orders = Orders.objects.filter(invtype = type_id, is_bid = False, mapsolarsystem__security_level__gte = min_sec, generated_at__gte = filter_time).order_by('price')[:50]
    
    rcontext = RequestContext(request, {'sell_orders':sell_orders, 'type_id':type_id})
    
    return render_to_response('market/quicklook/_quicklook_ask_filter.haml', rcontext)
    
def quicklook_bid_filter(request, type_id = 34, min_sec = 0, max_age = 8):
    """
    Returns quicklook partial for filtering
    """
    
    min_sec = float(min_sec) / 10
    if min_sec == 0:
        min_sec = -10
    
    filter_time = datetime.now() - timedelta(hours = int(max_age))
    
    # Fetch all buy orders from DB
    buy_orders = Orders.objects.filter(invtype = type_id, is_bid = True, mapsolarsystem__security_level__gte = min_sec, generated_at__gte = filter_time).order_by('-price')[:50]
    
    rcontext = RequestContext(request, {'buy_orders':buy_orders, 'type_id':type_id})
    
    return render_to_response('market/quicklook/_quicklook_bid_filter.haml', rcontext)