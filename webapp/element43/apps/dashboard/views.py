# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

# Django Aggregation
from django.db.models import Sum

# Models
from apps.api.models import Character, APITimer, CharSkill, MarketTransaction
from apps.feedreader.models import FeedItem

# Util
from apps.common.util import validate_characters, calculate_character_access_mask
from apps.dashboard.util import calculate_profit_stats


@login_required
def dashboard(request):
    """
    Shows basic information about you account so you can quickly get an overview.
    """

    # Get 10 latest news items
    news_items = FeedItem.objects.order_by('-published')[:10]

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

    rcontext = RequestContext(request, {'news_items': news_items,
                                        'sheet_data': sheet_data,
                                        'month': month,
                                        'week': week,
                                        'day': day,
                                        'last_ten_sales': last_ten_sales})

    return render_to_response('dashboard.haml', rcontext)

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
