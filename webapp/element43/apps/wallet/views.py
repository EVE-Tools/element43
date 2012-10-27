# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# Type Model
from eve_db.models import InvType

# API Models
from apps.api.models import MarketOrder, JournalEntry, MarketTransaction

# Utils
from apps.common.util import validate_characters, calculate_character_access_mask


def wallet(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['WalletJournal', 'WalletTransactions']))

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


def type(request, type_id):

    type_object = InvType.objects.get(id=type_id)

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['WalletTransactions']))

    transactions = MarketTransaction.objects.filter(character__in=chars,
                                                    invtype_id=type_id).extra(select={'revenue': "price * quantity"}).order_by('-date')

    # Calculate stats
    spent = 0
    income = 0
    profit = 0

    for transaction in transactions:
        if transaction.is_bid:
            spent += transaction.revenue
        else:
            income += transaction.revenue

    profit = income - spent

    # Add data to context
    rcontext = RequestContext(request, {'type': type_object,
                                        'spent': spent,
                                        'income': income,
                                        'profit': profit,
                                        'transactions': transactions})

    return render_to_response('wallet/type.haml', rcontext)
