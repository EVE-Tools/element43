# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count

# eve_db models
from apps.market_data.models import Orders
from eve_db.models import StaStation

# Time
import datetime

# Helper functions
from apps.market_data.util import group_breadcrumbs

def ranking(request, group = 0):
	"""
	This file generates the station ranks based on active orders in the DB
	"""
	
	rank_list = Orders.objects.values('stastation__name').annotate(ordercount=Count('id')).order_by('-ordercount')[:50]

	generated_at = datetime.datetime.now()
	rcontext = RequestContext(request, {'rank_list': rank_list, 'generated_at': generated_at})

	return render_to_response('trading/station/ranking.haml', rcontext)