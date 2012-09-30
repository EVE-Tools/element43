# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

# eve_db models
from eve_db.models import InvType
from eve_db.models import InvMarketGroup
from eve_db.models import EveIcon

# Models
from apps.market_data.models import Orders

# Helper functions
from apps.market_data.util import group_ids
import re

# JSON
from django.utils import simplejson

def tree(request, group = 0):
	"""
	Returns groups in JSON format for tree view.
	"""
		
	groups = []
		
	if group == 0:
			
		# Default to root groups
		groups = InvMarketGroup.objects.extra(where={'"parent_id" IS NULL'})
		group_json = []
		
		for group in groups:
			
			icon_name = "/static/images/icons/eve/22_32_42.png"
			group_json.append({'title': group.name,
								'key': str(group.id),
								'icon': icon_name,
								'isLazy': True,
								'isFolder': True,
								'noLink': True})
								
		group_json = simplejson.dumps(group_json)
		return HttpResponse(group_json, mimetype = 'application/json')
			
	else:

		group_json = []
		groups = InvMarketGroup.objects.filter(parent = group)

		for group in groups:
				
			icon_name = "/static/images/icons/eve/22_32_42.png"
				
			if group.has_items:
				group_json.append({'title': group.name,
									'key': str(group.id),
									'icon': icon_name,
									'hasItems': True,
									'isFolder': False,
									'noLink': False})
			else:
				group_json.append({'title': group.name,
									'key': str(group.id),
									'isLazy': True,
									'icon': icon_name,
									'isFolder': True,
									'noLink': True})
						
		group_json = simplejson.dumps(group_json)
		return HttpResponse(group_json, mimetype = 'application/json')
		
def panel(request, group = 0):
	"""
	Render panel.
	"""
	# Check if group is defined
	prices = {}
	
	types = InvType.objects.filter(market_group = group, is_published = True)
	
	for item in types:
		try:
			ask = Orders.objects.filter(invtype = item, is_bid = False).order_by("price")[:1][0].price
		except:
			ask = 0
				
		try:
			bid = Orders.objects.filter(invtype = item, is_bid = True).order_by("-price")[:1][0].price
		except:
			bid = 0
				
		prices.update({item.id:{'ask':ask, 'bid':bid}})
			
	# If there are types in this group render type template
	rcontext = RequestContext(request, {'parent_name':InvMarketGroup.objects.get(id = group).name, 'types':InvType.objects.filter(market_group = group, is_published = True), 'prices':prices})
	return render_to_response('market/browser/types.haml', rcontext)

def browser(request, group = 0):
	"""
	Market browser.
	"""
	
	if not group == 0:
		# If there is a group, add data to initialize tree
		
		breadcrumbs = group_ids(group)
		path = ""
		
		for crumb in breadcrumbs:
			path = path + '/' + str(crumb) 
		
		rcontext = RequestContext(request, {'path':path})
		return render_to_response('market/browser/browse.haml', rcontext)
	
	else:
		rcontext = RequestContext(request, {})
		return render_to_response('market/browser/browse.haml', rcontext)