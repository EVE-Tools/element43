# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# market_data models
from apps.market_data.models import Orders

# eve_db models
from eve_db.models import InvType
from eve_db.models import MapRegion

def random(request):
    
        # Get 25 random types from DB
        types = []
        types += InvType.objects.filter(is_published = True, market_group__isnull = False).order_by('?')[:25]

        rcontext = RequestContext(request, {'types':types})

        return render_to_response('market/scanners/randomscanner.haml', rcontext)

def region(request):
        if 'HTTP_EVE_REGIONID' in request.META:
            if MapRegion.objects.get(id = request.META['HTTP_EVE_REGIONID']) != None:
                # Pick types based on region and age
                types = []
                orders = []
            
                # Get all orders in this region ordered by age (limit to 1500 for performance)
                orders += Orders.objects.filter(mapregion = MapRegion.objects.get(id = request.META['HTTP_EVE_REGIONID'])).order_by('generated_at')[:1500]
            
                print len(orders)
            
                # Collect as many types as possible until we reach 50
                counter = 0
                for order in orders:
                        counter += 1
                        if not order.invtype in types:
                            types.append(order.invtype)
                        if len(types) >= 50:
                            break
            
                print counter

                rcontext = RequestContext(request, {'types':types, 'region':MapRegion.objects.get(id = request.META['HTTP_EVE_REGIONID'])})
            else:
                # Else do nothing
                rcontext = RequestContext(request, {})

            return render_to_response('market/scanners/regionscanner.haml', rcontext)
            
        rcontext = RequestContext(request, {})
        return render_to_response('home.haml', rcontext)
