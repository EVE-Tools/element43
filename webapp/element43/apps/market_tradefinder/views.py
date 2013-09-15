# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.utils import simplejson

from forms import TradefinderForm

from django.http import HttpResponse
from eve_db.models import MapRegion

from apps.market_data.models import Orders

from apps.market_tradefinder.sql import find_trades


def tradefinder(request):
    """
    Trade browser root.
    """

    if request.method == 'POST':  # If the form has been submitted...
        form = TradefinderForm(request.POST)  # A form bound to the POST data
        if form.is_valid():

            # All validation rules pass

            # Collect values
            start = form.cleaned_data.get('start')
            destination = form.cleaned_data.get('destination')

            # Get types worth trading
            trades = find_trades(start.id, destination.id)
            annotated_trades = []

            # Load additional data like top 5 orders
            for trade in trades:

                trade['top_buy'] = Orders.active.filter(mapregion=start, invtype_id=trade['id'], is_bid=True).order_by('price')[:5]
                trade['top_sell'] = Orders.active.filter(mapregion=destination, invtype_id=trade['id'], is_bid=False).order_by('-price')[:5]

                annotated_trades.append(trade)

            rcontext = RequestContext(request, {'trades': annotated_trades, 'start': start, 'destination': destination})
            return render_to_response('tradefind_result.haml', rcontext)
    else:
        form = TradefinderForm()

    rcontext = RequestContext(request, {})
    return render_to_response('start.haml', {'form': form}, rcontext)


def region_json(request):
    """
    Returns all region names as JSON for the finder typeahead.
    """

    # Prepare list
    data = []

    # Load data
    regions = MapRegion.objects.all()

    # Add name to list
    for region in regions:
        data.append(region.name)

    json = simplejson.dumps(data)

    # Return JSON without using any template
    return HttpResponse(json, mimetype='application/json')

