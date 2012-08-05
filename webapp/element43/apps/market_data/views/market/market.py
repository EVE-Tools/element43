# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# Aggregation
from django.db.models import Sum

# market_data models
from apps.market_data.models import Orders

# eve_db models
from eve_db.models import InvType
from eve_db.models import MapRegion

# numpy processing imports
import numpy as np

# Helper functions
from apps.market_data.util import group_breadcrumbs

def quicklook(request, type_id = 34):
		
		"""
		Generates a market overview for a certain type. Default to tritanium.
		"""
		
		# Get requested type
		type_object = InvType.objects.get(id = type_id)
		
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
			
			# Order of array entries: Name, Bid/Ask(Low, High, Average, Median, Standard Deviation, Lots, Volume)
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
			else:
				# Else there are no orders in this region -> add a bunch of 0s
				temp_data.extend([0,0,0,0,0,0,0])
			
			if len(region_bid_prices) > 0:
				# Bid values calculated via numpy
				temp_data.append(np.min(region_bid_prices))
				temp_data.append(np.max(region_bid_prices))
				temp_data.append(round(np.average(region_bid_prices),2))
				temp_data.append(np.median(region_bid_prices))
				temp_data.append(round(np.std(region_bid_prices),2))
				temp_data.append(len(region_bid_prices))
				temp_data.append(Orders.objects.filter(mapregion_id = region, invtype = type_id, is_bid = True).aggregate(Sum('volume_remaining'))['volume_remaining__sum'])
			else:
				# Else there are no orders in this region -> add a bunch of 0s
				temp_data.extend([0,0,0,0,0,0,0])
				
			# Append temp_data to region_data
			region_data.append(temp_data)
		
		breadcrumbs = group_breadcrumbs(type_object.market_group_id)
		# Use the 50 'best' orders for quicklook and add the region_data to the context
		rcontext = RequestContext(request, {'type':type_object, 'buy_orders':buy_orders[:50], 'sell_orders':sell_orders[:50], 'regions':region_data, 'breadcrumbs':breadcrumbs})
		
		return render_to_response('market/quicklook.haml', rcontext)