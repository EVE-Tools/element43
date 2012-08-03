# Template and HTTP handling
from django.shortcuts import render_to_response
from django.template import RequestContext

# market_data models
from models import Orders

# eve_db models
from eve_db.models import InvType
from eve_db.models import MapRegion

def random(request):
	
		# Get 25 random types from DB
		types = []
		types += InvType.objects.filter(is_published = True, market_group__isnull = False).order_by('?')[:25]

		rcontext = RequestContext(request, {'types':types})

		return render_to_response('market/randomscanner.haml', rcontext)

def region(request):
	
		if MapRegion.objects.get(id = request.META['HTTP_EVE_REGIONID']) != None:
			# Pick types based on region and age
			types = []
			orders = []
			
			# Get the 300 oldest orders in current region
			# Currently we need this large number until we can get distnict types.
			orders += Orders.objects.filter(mapregion = MapRegion.objects.get(id = request.META['HTTP_EVE_REGIONID'])).order_by('generated_at')[:300]
			
			# Get the types of the orders and add them to the type array if they're not already in there
			for order in orders:
					if not order.invtype in types:
						types.append(order.invtype)

			rcontext = RequestContext(request, {'types':types, 'region':MapRegion.objects.get(id = request.META['HTTP_EVE_REGIONID'])})
		else:
			# Else do nothing
			rcontext = RequestContext(request, {})

		return render_to_response('market/regionscanner.haml', rcontext)
