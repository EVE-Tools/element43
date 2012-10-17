# Template and context-related imports
from django.http import HttpResponse

# JSON for the live search
from django.utils import simplejson

# Models
from eve_db.models import InvBlueprintType


def blueprint_search(request):
    """
    Adds the blueprint search to the first form of the manufacturing calculator.
    """

    query = request.GET.get('query', '')

    # Prepare lists
    types = []
    type_names = []
    type_ids = []

    # Default to empty array
    types_json = "{query:'" + query + "', suggestions:[], data:[]}"

    # Only if the string is longer than 2 characters start looking in the DB
    if len(query) > 2:

        # Load published type objects matching the name
        blueprints = InvBlueprintType.objects.select_related()
        blueprints = blueprints.filter(
            blueprint_type__name__icontains=query,
            product_type__is_published=True,
            blueprint_type__is_published=True
        )

        for blueprint in list(blueprints):
            type_names.append(blueprint.blueprint_type.name)
            type_ids.append(blueprint.blueprint_type.id)

        # Add additional data for Ajax AutoComplete
        types_json = {'query': query, 'suggestions': type_names, 'data': type_ids}

        # Turn names into JSON
        types_json = simplejson.dumps(types_json)

    # Return JSON without using any template
    return HttpResponse(types_json, mimetype='application/json')
