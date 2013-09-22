# Utility
import time
import datetime
from django.utils import simplejson

# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

# Django Aggregation
from django.db.models import Sum

# API Models
from element43.apps.api.models import JournalEntry
from apps.api.models import Character, APITimer, CharSkill, MarketTransaction

# Util
from apps.common.util import validate_characters, calculate_character_access_mask
from apps.dashboard.util import calculate_profit_stats


@login_required
def dashboard(request):
    """
    Shows basic information about you account so you can quickly get an overview.
    """

    # Sheet based data
    chars_sheet = validate_characters(request.user, calculate_character_access_mask(['CharacterSheet']))
    sheet_data = []

    for char in chars_sheet:
        sheet_data.append({'char': char, 'next_update': APITimer.objects.get(character_id=char.id,
                                                                              apisheet='CharacterSheet').nextupdate})

    # Get all WalletJournal/WalletTransactions Chars
    market_chars = validate_characters(request.user, calculate_character_access_mask(['WalletJournal', 'WalletTransactions']))

    # Collect stats
    month = calculate_profit_stats(market_chars, 30)
    week = calculate_profit_stats(market_chars, 7)
    day = calculate_profit_stats(market_chars, 1)

    last_ten_sales = MarketTransaction.objects.filter(character__in=market_chars, is_bid=False).extra(select={'value': "price * quantity"}).order_by('-date')[:10]

    rcontext = RequestContext(request, {'sheet_data': sheet_data,
                                        'month': month,
                                        'week': week,
                                        'day': day,
                                        'last_ten_sales': last_ten_sales})

    return render_to_response('dashboard.haml', rcontext)


@login_required
def journal_json(request):
    # Get all chars with journal permissions
    chars = validate_characters(request.user, calculate_character_access_mask(['WalletJournal']))

    wallet_series = {}

    # Append wallet history of all characters to dict
    for char in chars:
        series = []
        journal = JournalEntry.objects.filter(character=char).order_by('date')

        for point in journal:
            series.append([int(time.mktime(point.date.timetuple())) * 1000, point.balance])

        # If there aren't any journal entries, catch the resulting AssertionError and return empty list
        try:
            # Add current balance in the end for a more consistent look
            series.append([(int(time.mktime(datetime.datetime.utcnow().timetuple())) * 999), journal[len(journal) - 1].balance])
        except AssertionError:
            series = []

        wallet_series[char.name] = series

    json = simplejson.dumps(wallet_series)

    # Return JSON without using any template
    return HttpResponse(json, mimetype='application/json')


@login_required
def char_sheet(request, char_id):

    try:
        char = Character.objects.get(user=request.user, id=char_id)
    except:
        messages.error(request, 'There is no such character in our database.')
        return HttpResponseRedirect(reverse('home'))

    # Get skills
    skills = CharSkill.objects.filter(character_id=char.id).order_by('skill__group')

    skill_points = CharSkill.objects.filter(character_id=char.id).aggregate(Sum('skillpoints'))['skillpoints__sum']

    rcontext = RequestContext(request, {'char': char, 'skills': skills, 'skill_points': skill_points})
    return render_to_response('_char_sheet.haml', rcontext)
