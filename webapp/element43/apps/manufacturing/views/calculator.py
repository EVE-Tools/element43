# Django imports
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.manufacturing.functions import calculate_manufacturing_job, update_blueprint_history

# App settings
from apps.manufacturing.settings import MANUFACTURING_MAX_BLUEPRINT_HISTORY, MANUFACTURING_BLUEPRINT_HISTORY_SESSION

# Forms
from apps.manufacturing.forms import SelectBlueprintForm, ManufacturingCalculatorForm

from apps.api.models import Character

# Models
from eve_db.models import InvBlueprintType
from apps.market_data.models import ItemRegionStat

from eveigb import IGBHeaderParser

def select_blueprint(request):
    """
    View to search for a blueprint. If only one blueprint is found the user will be
    redirected immediately to the calculator. Otherwise he will be shown a list of
    all found blueprints and has to select the one he wants to produce.
    """

    template_vars = {}

    # When the user selects a new blueprint we better delete the settings he used for
    # his last calculation.
    if request.session.get('form_data'):
        del request.session['form_data']

    if request.method == 'POST':
        form = SelectBlueprintForm(request.POST)

        if form.is_valid():
            blueprint_name = form.cleaned_data['blueprint']
            blueprints = InvBlueprintType.objects.filter(blueprint_type__name__icontains=blueprint_name)

            if len(blueprints) == 1:
                return HttpResponseRedirect(reverse('manufacturing_calculator',
                                            kwargs={'blueprint_type_id': blueprints[0].blueprint_type.id}))

            # If more than one result was found all blueprints are added to the
            # request context. The select_blueprint.haml will be rendered again
            # but now with a list of found blueprints.
            template_vars['blueprints'] = blueprints

    template_vars['form'] = SelectBlueprintForm()
    template_vars['MANUFACTURING_MAX_BLUEPRINT_HISTORY'] = MANUFACTURING_MAX_BLUEPRINT_HISTORY
    template_vars[MANUFACTURING_BLUEPRINT_HISTORY_SESSION] = request.session.get(MANUFACTURING_BLUEPRINT_HISTORY_SESSION, None)

    rcontext = RequestContext(request, template_vars)
    return render_to_response('select_blueprint.haml', rcontext)


def calculator(request, blueprint_type_id):
    """
    This view contains the form where the user types in all the relevant data
    that is needed to calculate the manufacturing job.
    """
    try:
        blueprint = InvBlueprintType.objects.get(pk=blueprint_type_id)
        update_blueprint_history(request, blueprint)
    except InvBlueprintType.DoesNotExist:
        # There is no blueprint with the given id. Go back to start!
        return HttpResponseRedirect(reverse('manufacturing_select_blueprint'))

    if request.method == 'POST':
        form = ManufacturingCalculatorForm(request.user, request.POST)

        if form.is_valid():
            # Put the form data in the session. If the user goes back to change the "job" information
            # the form will have those information as initial data!
            request.session['form_data'] = request.POST
            form.cleaned_data['blueprint_type_id'] = blueprint_type_id
            data = calculate_manufacturing_job(form.cleaned_data)

            rcontext = RequestContext(request, {'data': data})
            return render_to_response('manufacture_result.haml', rcontext)
    else:
        if request.session.get('form_data'):
            form = ManufacturingCalculatorForm(request.user, request.session.get('form_data'))
        else:
            # find the sale price for the product
            try:
                stat_object = ItemRegionStat.objects.get(invtype_id__exact=blueprint.product_type.id, mapregion_id__exact=10000002)
                target_sell_price = stat_object.sell_95_percentile
            except ItemRegionStat.DoesNotExist:
                target_sell_price = 0

            initial_data = {'target_sell_price': "%.2f" % target_sell_price}

            headers = IGBHeaderParser(request)
            if headers.is_igb and headers.charid != 0:
                initial_data['character'] = headers.charid

            form = ManufacturingCalculatorForm(request.user, initial=initial_data)

    rcontext = RequestContext(request, {'form': form, 'blueprint': blueprint})
    return render_to_response('jobparameter.haml', rcontext)
