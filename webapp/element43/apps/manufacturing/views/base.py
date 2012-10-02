# Template and context-related imports
from django.http import HttpResponse

# JSON for the live search
from django.utils import simplejson

# Models
from eve_db.models import InvBlueprintType

def blueprint_search(request):
    """
    This adds a basic live search view to element43.
    The names in the invTypes table are searched with a case insensitive LIKE query and the result is returned as a JSON array of matching names.
    """

    if request.GET.get('query'):
        query = request.GET.get('query')
    else:
        query = ""

    # Prepare lists
    types = []
    type_names = []
    type_ids = []

    # Default to empty array
    types_json = "{query:'" + query + "', suggestions:[], data:[]}"

    # Only if the string is longer than 2 characters start looking in the DB
    if len(query) > 2:

        # Load published type objects matching the name
        types = InvBlueprintType.objects.filter(blueprint_type__name__icontains = query, product_type__is_published = True, blueprint_type__is_published = True)

        for single_type in types:
            type_names.append(single_type.blueprint_type.name)
            type_ids.append(single_type.blueprint_type.id)

        # Add additional data for Ajax AutoComplete
        types_json = {'query': query, 'suggestions': type_names, 'data': type_ids}

        # Turn names into JSON
        types_json = simplejson.dumps(types_json)

    # Return JSON without using any template
    return HttpResponse(types_json, mimetype = 'application/json')