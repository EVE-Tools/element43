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
from apps.api.models import Character, APITimer, CharSkill, MarketOrder, JournalEntry
from apps.common.util import validate_characters


@login_required
def dashboard(request):
    """
    Shows basic information about you account so you can quickly get an overview.
    """

    # Sheet based data
    chars_sheet = validate_characters(request.user, 8)
    sheet_data = []

    for char in chars_sheet:
        sheet_data.append({'char': char, 'next_update': APITimer.objects.get(character_id=char.id,
                                                                              apisheet='CharacterSheet').nextupdate})

    # Order based data
    chars_order = validate_characters(request.user, 4096)
    market_data = {}

    market_data['ask'] = []
    market_data['ask_volume'] = 0

    market_data['bid'] = []
    market_data['bid_volume'] = 0

    market_data['total_volume'] = 0

    # Calculate volumes
    for char in chars_order:
        market_data['ask'] += MarketOrder.objects.filter(character=char, order_state=0, id__is_bid=False)
        market_data['bid'] += MarketOrder.objects.filter(character=char, order_state=0, id__is_bid=True)

    for order in market_data['ask']:
        market_data['ask_volume'] += order.id.price * order.id.volume_remaining

    for order in market_data['bid']:
        market_data['bid_volume'] += -1 * order.id.price * order.id.volume_remaining

    market_data['total_volume'] = market_data['ask_volume'] + market_data['bid_volume']

    rcontext = RequestContext(request, {'sheet_data': sheet_data, 'market_data': market_data})
    return render_to_response('dashboard/dashboard.haml', rcontext)


@login_required
def journal_json(request):
    # Get all chars with journal permissions
    chars = validate_characters(request.user, 2097152)

    wallet_series = {}

    # Append wallet history of all characters to dict
    for char in chars:
        series = []
        journal = JournalEntry.objects.filter(character=char).order_by('date')

        for point in journal:
            series.append([int(time.mktime(point.date.timetuple())) * 1000, point.balance])

        # Add current balance in the end for a more consistent look
        series.append([(int(time.mktime(datetime.datetime.utcnow().timetuple())) * 1000), journal[len(journal) - 1].balance])

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
    return render_to_response('dashboard/_char_sheet.haml', rcontext)
