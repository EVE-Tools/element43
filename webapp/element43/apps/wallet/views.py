# Template and context-related imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext

# Type Model
from eve_db.models import InvType

from element43.apps.api.models import Character
# API Models
from apps.api.models import MarketOrder, JournalEntry, MarketTransaction, RefType

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


def transactions(request, char_id):

    # Get all characters with sufficient permissions
    char = Character.objects.get(id=char_id)

    all_transactions = MarketTransaction.objects.filter(character=char).extra(select={'revenue': "price * quantity"}).order_by('-date')

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

    # Add data to context
    rcontext = RequestContext(request, {'transactions': transactions, 'char': char})
    return render_to_response('wallet/transactions.haml', rcontext)


def journal(request, char_id):

    # Get all characters with sufficient permissions
    char = Character.objects.get(id=char_id)
    ref_id = request.GET.get('ref_id')

    # Apply refID filter, if supplied
    if ref_id:
        # If we don't have a numerical input, default to all transactions
        try:
            all_journal_entries = JournalEntry.objects.filter(character=char, ref_type_id=ref_id).order_by('-date')
        except ValueError:
            all_journal_entries = JournalEntry.objects.filter(character=char).order_by('-date')
    else:
        # Simply get all transactions if no filter was supplied
        all_journal_entries = JournalEntry.objects.filter(character=char).order_by('-date')

    # Get refTypes for dropdown list
    ref_types = RefType.objects.exclude(name='').order_by('name')

    # Pagination
    paginator = Paginator(all_journal_entries, 25)

    page = request.GET.get('page')
    try:
        journal_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        journal_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        journal_entries = paginator.page(paginator.num_pages)

    # Add data to context
    rcontext = RequestContext(request, {'journal': journal_entries, 'char': char, 'ref_types': ref_types})

    return render_to_response('wallet/journal.haml', rcontext)


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


def station_scanner(request, station_id):

    # Get all characters with sufficient permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['MarketOrders']))

    # Get types of active orders in that station from db
    types = []
    type_ids = []

    orders = MarketOrder.objects.filter(character__in=chars, order_state=0, id__stastation=station_id).distinct('id__invtype')

    for order in orders:
        type_ids.append(order.id.invtype.id)

    for type_object in types:
        type_ids.append(type_object.id)

    rcontext = RequestContext(request, {'type_ids': type_ids})

    return render_to_response('wallet/scanner.haml', rcontext)


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
