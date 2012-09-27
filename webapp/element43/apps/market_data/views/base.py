# Template and context-related imports
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

# JSON for the live search
from django.utils import simplejson

# Models
from eve_db.models import InvType
from apps.market_data.models import Orders, OrdersWarehouse, History, ItemRegionStat, ItemRegionStatHistory, EmdrStats

# Utils
import datetime

"""
Those are our views. We have to use the RequestContext for CSRF protection, 
since we have a form (search) in every single of our views, as they extend 'base.haml'.
"""

def home(request):
	
	"""
	Returns our static home template with a CSRF protection for our search as well as the stats.
	"""
	
	# Create context for CSRF protection
	rcontext = RequestContext(request, {})
	
	return render_to_response('home.haml', rcontext)
	
def stats(request):
	"""
	Returns stats page
	"""
	
	# Collect stats
	
	# 1. Platform stats
	active_orders = Orders.objects.count()
	archived_orders = OrdersWarehouse.objects.count()
	history = History.objects.count()
	
	new_orders_per_minute = EmdrStats.objects.filter(status_type = 1).order_by("message_timestamp")[:1][0].status_count / 5
	updated_orders_per_minute = EmdrStats.objects.filter(status_type = 2).order_by("message_timestamp")[:1][0].status_count / 5
	old_orders_per_minute = EmdrStats.objects.filter(status_type = 3).order_by("message_timestamp")[:1][0].status_count / 5
	
	history_messages_per_minute = EmdrStats.objects.filter(status_type = 1).order_by("message_timestamp")[:1][0].status_count / 5
	
	# 2. Minerals and PLEX
	types = [34,35,36,37,38,39,40,29668]
	region = 10000002
	typestats = []
	
	for item in types:
		
		# Still works if we have no data for that item
		try:
			region_stats = ItemRegionStat.objects.filter(mapregion_id = region, invtype_id = item).order_by("lastupdate")[:1][0]
			region_stats_history = ItemRegionStatHistory.objects.filter(mapregion_id = region, invtype_id = item).order_by("date")[:1][0]
			stats = {'buy': region_stats.buymean,
					 'buy_move': region_stats_history.buymean - region_stats.buymean,
					 'sell': region_stats.sellmean,
					 'sell_move': region_stats_history.sellmean - region_stats.sellmean,
					 'mean': (region_stats.buymean + region_stats.sellmean) / 2,
					 'mean_move': ((region_stats_history.buymean + region_stats_history.sellmean) / 2) - ((region_stats.buymean + region_stats.sellmean) / 2)}
		
			typestats.append({'type':InvType.objects.get(id = item), 'stats':stats})
		
		except:
			pass
	
	
	# Create context for CSRF protection
	rcontext = RequestContext(request, {'active_orders': active_orders, 
										'archived_orders': archived_orders, 
										'history': history, 
										'new_orders_per_minute':new_orders_per_minute,
										'updated_orders_per_minute':updated_orders_per_minute, 
										'old_orders_per_minute':old_orders_per_minute, 
										'history_messages_per_minute': history_messages_per_minute,
										'typestats': typestats,
										'update': datetime.datetime.now()})
	return render_to_response('stats.haml', rcontext)
	
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
		types = InvType.objects.filter(name__icontains = query, is_published = True, market_group__isnull = False)
			
	# If there is only one hit, directly redirect to quicklook
	if len(types) == 1:
		type_id = str(types[0].id)
		print type_id
		return HttpResponseRedirect('/market/' + type_id)
			
	# Create Context
	rcontext = RequestContext(request, {'types':types})		
	
	# Render template
	return render_to_response('search.haml', rcontext)
	
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
	types = []
	type_names = []
	type_ids = []
	
	# Default to empty array
	types_json = "{query:'" + query + "', suggestions:[], data:[]}"
	
	# Only if the string is longer than 2 characters start looking in the DB
	if len(query) > 2:
		
		# Load published type objects matching the name
		types = InvType.objects.filter(name__icontains = query, is_published = True, market_group__isnull = False)
		
		for single_type in types:
			type_names.append(single_type.name)
			type_ids.append(single_type.id)
		
		# Add additional data for Ajax AutoComplete
		types_json = {'query': query, 'suggestions': type_names, 'data': type_ids}
		
		# Turn names into JSON
		types_json = simplejson.dumps(types_json)
	
	# Return JSON without using any template
	return HttpResponse(types_json, mimetype = 'application/json')
