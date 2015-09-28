# Utils
import ujson as ujson

# Imports for memcache
import pylibmc
from apps.common.util import get_memcache_client, dictfetchall

# Template and context-related imports
from django.db import connection
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages

# JSON for the live search
import json

# Models
from eve_db.models import InvType, StaStation
from apps.market_data.models import Orders, ItemRegionStat, ItemRegionStatHistory, EmdrStats

"""
Those are our views. We have to use the RequestContext for CSRF protection,
since we have a form (search) in every single of our views, as they extend 'base.haml'.
"""


def home(request):

    """
    Returns our static home template with a CSRF protection for our search as well as the stats layout.
    """

    type_ids = [34, 35, 36, 37, 38, 39, 40, 29668]
    region = 10000002

    types = InvType.objects.filter(id__in=type_ids)

    #
    # Preload cached stats
    #

    # Connect to memcache
    mc = get_memcache_client()

    typestats = {}

    if (mc.get("e43-fullstats") is not None):

        initial_stats = ujson.loads(mc.get("e43-fullstats"))

    else:

        # Load empty values

        for invtype in types:

            stats = {'bid_median': 0,
                     'bid_median_move': 0,
                     'ask_median': 0,
                     'ask_median_move': 0}

            if stats:
                typestats[invtype] = stats

        initial_stats = {'typestats': typestats}

    # Create context for CSRF protection
    rcontext = RequestContext(request, {'type_ids': type_ids, 'types': types, 'region': region, 'stats': initial_stats})

    return render_to_response('home.haml', rcontext)


def about_page(request):

    """
    Returns the about page with information about the site and contact information
    """

    rcontext = RequestContext(request, {})

    return render_to_response('about_page.haml', rcontext)


def api_docs(request):

    """
    Returns the about page with information about the API
    """

    rcontext = RequestContext(request, {})

    return render_to_response('api_docs.haml', rcontext)


def stats_json(request, region_id):

    """
    Returns stat JSON for the front page
    """

    # Connect to memcache
    mc = get_memcache_client()

    # Minerals and PLEX
    types = request.GET.getlist('type')
    new_types = []

    for item in types:
        new_types.append(int(item))

    types = new_types
    typestats = {}
    cache_item = {}
    buymedian = 0
    sellmedian = 0

    for item in types:

        # Still works in case we have no data for that item
        try:
            # check to see if it's in the cache, if so use those values
            if (mc.get("e43-stats" + str(item)) is not None):
                cache_item = ujson.loads(mc.get("e43-stats" + str(item)))
                buymedian = cache_item['buymedian']
                sellmedian = cache_item['sellmedian']
            # otherwise go to the DB for it
            else:

                # Catch error if we don't have any data for that type
                try:
                    region_stats = ItemRegionStat.objects.filter(mapregion_id=region_id, invtype_id=item)[:1][0]
                    buymedian = region_stats.buymedian
                    sellmedian = region_stats.sellmedian

                except:
                    buymedian = 0
                    sellmedian = 0

            region_stats_history = ItemRegionStatHistory.objects.filter(mapregion_id=region_id, invtype_id=item).order_by("-date")[:1][0]


            stats = {'bid_median': buymedian,
                     'bid_median_move': region_stats_history.buymedian - buymedian,
                     'ask_median': sellmedian,
                     'ask_median_move': region_stats_history.sellmedian - sellmedian}

            if stats:
                typestats[item] = stats

        except pylibmc.Error as e:
            print e

    # Create JSON
    stat_json = json.dumps({'typestats': typestats})

    # Save complete stats to memcached
    mc.set("e43-fullstats", stat_json)

    # Return JSON without using any template
    return HttpResponse(stat_json, content_type='application/json')


def search(request):

    """
    This adds a basic search view to element43.
    The names in the invTypes table are searched with a case insensitive LIKE query.
    """

    # Get query from request
    query = request.POST.get('query', '')

    # Prepare list
    types = []
    stations = []

    # Only if the string is longer than 2 characters start looking in the DB
    if len(query) > 2:

        # Load published type objects matching the name
        types = InvType.objects.filter(name__icontains=query, is_published=True, market_group__isnull=False)

        # Load stations
        stations = StaStation.objects.filter(name__icontains=query)

    # If there is only one hit, directly redirect to quicklook
    if len(types) == 1 and len(stations) == 0:
        type_id = str(types[0].id)
        return HttpResponseRedirect(reverse('quicklook', kwargs={'type_id': type_id}))

    # If there is only one hit, directly redirect to import
    if len(stations) == 1 and len(types) == 0:
        station_id = str(stations[0].id)
        return HttpResponseRedirect(reverse('station', kwargs={'station_id': station_id}))

    # Create Context
    rcontext = RequestContext(request, {'types': types, 'stations': stations})

    # Render template
    return render_to_response('search.haml', rcontext)


def live_search(request):

    """
    This adds a basic live search view to element43.
    The names in the invTypes table are searched with a case insensitive LIKE query and the result is returned as a JSON array of matching names.
    """

    if request.GET.get('query'):
        query = request.GET.get('query')
    else:
        query = ""

    # Prepare lists
    names = []
    ids = []

    # Default to empty array
    search_json = "{query:'" + query + "', suggestions:[], data:[]}"

    # Only if the string is longer than 2 characters start looking in the DB
    if len(query) > 2:

        # Load published type objects matching the name
        types = InvType.objects.filter(name__icontains=query, is_published=True, market_group__isnull=False)

        for single_type in types:
            names.append(single_type.name)
            ids.append('type_' + str(single_type.id))

        # Load station
        stations = StaStation.objects.filter(name__icontains=query)

        for station in stations:
            names.append(station.name)
            ids.append('station_' + str(station.id))

        # Add additional data for Ajax AutoComplete
        search_json = {'query': query, 'suggestions': names, 'data': ids}

        # Turn names into JSON
        search_json = json.dumps(search_json)

    # Return JSON without using any template
    return HttpResponse(search_json, content_type='application/json')


def handler_403(request):

    """
    Redirects user home with an error message.
    """

    messages.warning(request, '403 - Forbidden. You were not supposed to access the page you tried to look at.')
    return HttpResponseRedirect(reverse('home'))


def handler_404(request):

    """
    Redirects user home with an error message.
    """

    messages.warning(
        request, '404 - The page you were looking for could not be found.')
    return HttpResponseRedirect(reverse('home'))


def handler_500(request):

    """
    Redirects user home with an error message.
    """

    messages.error(request, '500 - Internal server error. Looks like there is a bug in Element43. The error was logged and we will try to fix it soon.')
    return HttpResponseRedirect(reverse('home'))
