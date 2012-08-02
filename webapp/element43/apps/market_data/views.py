# Template and context-related imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

# Aggregation
from django.db.models import Sum

# JSON for the live search
from django.utils import simplejson

# market_data models
from models import Orders

# Helper functions
from util import group_breadcrumbs

# eve_db models
from eve_db.models import InvType
from eve_db.models import InvMarketGroup
from eve_db.models import MapRegion

# numpy processing imports
import numpy as np

"""
Those are our views. We have to use the RequestContext for CSRF protection, 
since we have a form (search) in every single of our views, as they extend 'base.haml'.
"""

def home(request):
		
		"""
		Returns our static home template with a CSRF protection for our search.
		"""
		
		# Create context for CSRF protection
		rcontext = RequestContext(request, {})
		
		return render_to_response('home.haml', rcontext)
		
def search(request):
	
		"""
		This adds a basic search view to element43.
		The names in the invTypes table are searched with a case insensitive LIKE query.
		"""
		
		# Get query from request
		query = request.POST.get('query', '')
		
		# Prepare list
		types = []
		
		# Only if the string is longer than 2 characters start looking in the DB
		if len(query) > 2:
			
				# Load published type objects matching the name
				types = InvType.objects.filter(name__icontains = query, is_published = True)
				
		# If there is only one hit, directly redirect to quicklook
		if len(types) == 1:
			type_id = str(types[0].id)
			print type_id
			return HttpResponseRedirect('/market/' + type_id)
				
		# Create Context
		rcontext = RequestContext(request, {'types':types})		
		
		# Render template
		return render_to_response('search.haml', rcontext)
		
def live_search(request, query='a'):
	
		"""
		This adds a basic live search view to element43.
		The names in the invTypes table are searched with a case insensitive LIKE query and the result is returned as a JSON array of matching names.
		"""
		
		# Prepare lists
		types = []
		type_names = []
		
		# Default to empty array
		types_json = "[]"
		
		# Only if the string is longer than 2 characters start looking in the DB
		if len(query) > 2:
			
				# Load published type objects matching the name
				types = InvType.objects.filter(name__icontains = query, is_published = True)
				
				for single_type in types:
					type_names.append(single_type.name)
				
				# Turn names into JSON
				types_json = simplejson.dumps(type_names)
		
		# Return JSON without using any template
		return HttpResponse(types_json, mimetype = 'application/json')
		
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
		
		return render_to_response('quicklook.haml', rcontext)
		
def browser(request, group = 0):
		"""
		This returns the groups/types in a group.
		There are three types of groups:
			1. Root groups. Their parent_id is NULL, since they are at the root of the tree.
			2. Groups in the middle of the tree. They originate from another group and contain other groups as well.
			3. Groups which contain types and originate from another group.
		"""
		groups = []
		
		if group == 0:
			
			# Default to root groups
			groups = InvMarketGroup.objects.extra(where={'"parent_id" IS NULL'})
			rcontext = RequestContext(request, {'groups':groups})
			return render_to_response('browse_root.haml', rcontext)
			
		elif InvMarketGroup.objects.get(id = group).has_items == True:
			
			# If there are types in this group render type template
			breadcrumbs = group_breadcrumbs(group)
			rcontext = RequestContext(request, {'parent_name':InvMarketGroup.objects.get(id = group).name, 'types':InvType.objects.filter(market_group = group), 'breadcrumbs':breadcrumbs})
			return render_to_response('browse_types.haml', rcontext)
			
		else:
			
			# 3'rd type
			breadcrumbs = group_breadcrumbs(group)
			groups = InvMarketGroup.objects.filter(parent = group)
			rcontext = RequestContext(request, {'parent': InvMarketGroup.objects.get(id = group), 'groups':groups, 'breadcrumbs':breadcrumbs})
			return render_to_response('browse_groups.haml', rcontext)
		