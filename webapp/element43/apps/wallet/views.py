# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# API Models
from apps.api.models import MarketOrder, JournalEntry, MarketTransaction

# Utils
from apps.common.util import validate_characters


def wallet(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, 6295552)

    # Prepare lists
    orders_bid = []
    orders_ask = []
    transactions = {}
    journal = {}

    # Get the data
    for char in chars:
        orders_bid += MarketOrder.objects.filter(character=char,
                                                 id__is_bid=True).select_related('id').extra(select={'total_value': "price * volume_entered",
                                                                                                     'total_value_remaining': "price * volume_remaining"}).order_by('order_state')

        orders_ask += MarketOrder.objects.filter(character=char,
                                                 id__is_bid=False).select_related('id').extra(select={'total_value': "price * volume_entered",
                                                                                                      'total_value_remaining': "price * volume_remaining"}).order_by('order_state')

        transactions[char.id] = MarketTransaction.objects.filter(character=char).select_related('ref_type')
        journal[char.id] = JournalEntry.objects.filter(character=char)

    # Add data to context
    rcontext = RequestContext(request, {'orders_bid': orders_bid,
                                        'orders_ask': orders_ask,
                                        'transactions': transactions,
                                        'journal': journal})

    return render_to_response('wallet/wallet.haml', rcontext)
