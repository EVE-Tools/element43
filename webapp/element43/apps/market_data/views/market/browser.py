# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# eve_db models
from eve_db.models import InvType
from eve_db.models import InvMarketGroup

# Models
from apps.market_data.models import Orders


def panel(request, group=0):
    """
    Render panel.
    """
    # Check if group is defined
    prices = {}

    types = InvType.objects.filter(market_group=group, is_published=True)

    for item in types:
        try:
            ask = Orders.active.filter(invtype=item, is_bid=False).order_by("price")[:1][0].price
        except:
            ask = 0

        try:
            bid = Orders.active.filter(invtype=item, is_bid=True).order_by("-price")[:1][0].price
        except:
            bid = 0

        prices.update({item.id: {'ask': ask, 'bid': bid}})

    # If there are types in this group render type template
    rcontext = RequestContext(request, {'parent_name': InvMarketGroup.objects.get(id=group).name,
                                        'types': InvType.objects.filter(market_group=group,
                                        is_published=True),
                                        'prices': prices})

    return render_to_response('browser/types.haml', rcontext)


def browser(request, group=0):
    """
    Market browser.
    """

    print group

    if not group == 0:
        # If there is a group, add data to initialize tree

        rcontext = RequestContext(request, {'market_group': group})
        return render_to_response('browser/browse.haml', rcontext)

    else:
        rcontext = RequestContext(request, {})
        return render_to_response('browser/browse.haml', rcontext)
