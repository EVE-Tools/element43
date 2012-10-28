# Template and context-related imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext

# Type Model
from eve_db.models import InvType

# API Models
from apps.api.models import MarketOrder, JournalEntry, MarketTransaction

# Utils
from apps.common.util import validate_characters, calculate_character_access_mask


def active_orders(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['MarketOrders']))

    # Get all active orders ordered by station for later regrouping
    orders = MarketOrder.objects.filter(character__in=chars, order_state=0).select_related('id').extra(select={'total_value': "price * volume_entered",
                                                                                                               'volume_percent': "(volume_remaining / volume_entered::float) * 100"}).order_by('id__stastation')

    # Add data to context
    rcontext = RequestContext(request, {'orders': orders})
    return render_to_response('wallet/active_orders.haml', rcontext)


def archived_orders(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['MarketOrders']))

    # Get all active orders ordered by station for later regrouping
    all_orders = MarketOrder.objects.filter(character__in=chars).exclude(order_state=0).select_related('id').order_by('-id__generated_at')

    # Pagination
    paginator = Paginator(all_orders, 25)

    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)

    # Add data to context
    rcontext = RequestContext(request, {'orders': orders})
    return render_to_response('wallet/archived_orders.haml', rcontext)


def transactions(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['WalletTransactions']))

    # Add data to context
    rcontext = RequestContext(request, {'transactions': transactions})
    return render_to_response('wallet/transactions.haml', rcontext)

def journal(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['WalletJournal']))

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

def wallet(request):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['WalletJournal']))

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

    all_transactions = MarketTransaction.objects.filter(character__in=chars,
                                                        invtype_id=type_id).extra(select={'revenue': "price * quantity"}).order_by('-date')

    # Pagination
    paginator = Paginator(all_transactions, 25)

    page = request.GET.get('page')
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        transactions = paginator.page(paginator.num_pages)

    # Calculate stats
    spent = 0
    income = 0
    profit = 0

    for transaction in all_transactions:
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
