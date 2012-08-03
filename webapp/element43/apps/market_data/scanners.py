# Template and HTTP handling
from django.shortcuts import render_to_response
from django.template import RequestContext

# eve_db models
from eve_db.models import InvType

def random(request):
		types = []
		types += (InvType.objects.filter(is_published = True, market_group__isnull = False).order_by('?')[:25])

		rcontext = RequestContext(request, {'types':types})

		return render_to_response('market/randomscanner.haml', rcontext)
