# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# market_data models
from apps.market_data.models import Orders

# eve_db models
from eve_db.models import InvType
from eve_db.models import MapRegion


def random(request):

        # Get 25 random types from DB
        types = []
        types += InvType.objects.filter(is_published=True, market_group__isnull=False).order_by('?')[:25]

        rcontext = RequestContext(request, {'types': types})

        return render_to_response('scanners/randomscanner.haml', rcontext)


def region(request):
        if 'HTTP_EVE_REGIONID' in request.META:
            if MapRegion.objects.get(id=request.META['HTTP_EVE_REGIONID']) != None:
                # Pick types based on region and age

                region = MapRegion.objects.get(id=request.META['HTTP_EVE_REGIONID'])

                # Get all orders in this region ordered by age
                type_ids = Orders.active.filter(mapregion=region).order_by('generated_at').values_list('invtype_id', flat=True).distinct()[:50]

                types = InvType.objects.filter(id__in=list(type_ids))

                rcontext = RequestContext(request, {'types': types, 'region': region})
                return render_to_response('scanners/regionscanner.haml', rcontext)
            else:
                messages.info(request, 'It seems like you did not grant trust to Element43 in the IGB.')
                return HttpResponseRedirect(reverse('home'))
        else:
            messages.info(request, 'It seems like you did not grant trust to Element43 in the IGB.')
            return HttpResponseRedirect(reverse('home'))
