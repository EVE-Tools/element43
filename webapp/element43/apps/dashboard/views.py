# Template and context-related imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

# Django Aggregation
from django.db.models import Sum

# API Models
from apps.api.models import Character, APITimer, CharSkill
from apps.common.util import validate_characters


@login_required
def dashboard(request):

    chars_market = validate_characters(request.user, 8)
    market_data = []

    for char in chars_market:
        market_data.append({'char': char, 'next_update': APITimer.objects.get(character_id=char.id,
                                                                              apisheet='CharacterSheet').nextupdate})

    rcontext = RequestContext(request, {'market_data': market_data})
    return render_to_response('dashboard/dashboard.haml', rcontext)


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
