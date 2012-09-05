# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# eve_db models
from eve_db.models import InvType
from eve_db.models import InvMarketGroup

# Helper functions
from apps.market_data.util import group_breadcrumbs

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
			return render_to_response('market/browser/root.haml', rcontext)
			
		elif InvMarketGroup.objects.get(id = group).has_items == True:
			
			# If there are types in this group render type template
			breadcrumbs = group_breadcrumbs(group)
			rcontext = RequestContext(request, {'parent_name':InvMarketGroup.objects.get(id = group).name, 'types':InvType.objects.filter(market_group = group, is_published = True), 'breadcrumbs':breadcrumbs})
			return render_to_response('market/browser/types.haml', rcontext)
			
		else:
			
			# 3'rd type
			breadcrumbs = group_breadcrumbs(group)
			groups = InvMarketGroup.objects.filter(parent = group)
			rcontext = RequestContext(request, {'parent': InvMarketGroup.objects.get(id = group), 'groups':groups, 'breadcrumbs':breadcrumbs})
			return render_to_response('market/browser/groups.haml', rcontext)