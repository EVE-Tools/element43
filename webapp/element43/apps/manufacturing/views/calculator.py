from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.manufacturing.functions import calculate_manufacturing_job

# Forms
from django import forms
from apps.manufacturing.forms import SelectBlueprintForm, ManufacturingCalculatorForm

# Models
from eve_db.models import InvType, InvBlueprintType

def select_blueprint(request):
    """
    View to select the blueprint.
    """
    if request.session.get('form_data'):
        del request.session['form_data']
    
    if request.method == 'POST':
        form = SelectBlueprintForm(request.POST)
        
        if form.is_valid():
            try:
                blueprint_name = form.cleaned_data['blueprint']
                blueprint = InvType.objects.get(name=blueprint_name)
            except InvType.DoesNotExist:
                raise forms.ValidationError("Could not find blueprint '%s'" % blueprint_name)

            return HttpResponseRedirect(reverse('manufacturing_calculator', kwargs={ 'blueprint_type_id': blueprint.id }))
    else:
        form = SelectBlueprintForm()
    
    rcontext = RequestContext(request, { 'form' : form })
    return render_to_response('manufacturing/forms/select_blueprint.haml', rcontext)

def calculator(request, blueprint_type_id):    
    """
    This view contains the form where the user types in all the relevant data
    that is needed to calculate the manufacturing job.
    """
    try:
        blueprint = InvBlueprintType.objects.get(pk=blueprint_type_id)
    except InvBlueprintType.DoesNotExist:
        # There is no blueprint with the give id. Go back to start!
        return HttpResponseRedirect(reverse('manufacturing_select_blueprint'))

    if request.method == 'POST':
        form = ManufacturingCalculatorForm(request.POST)
        
        if form.is_valid():
            # Put the form data in the session. If the user goes back to change the "job" information
            # the form will have those information as initial data!
            request.session['form_data'] = request.POST
            
            form.cleaned_data['blueprint_type_id'] = blueprint_type_id
            data = calculate_manufacturing_job(form.cleaned_data)
            rcontext = RequestContext(request, { 'data' : data })
            
            return render_to_response('manufacturing/forms/result.haml', rcontext)
    else:
        if request.session.get('form_data'):
            form = ManufacturingCalculatorForm(request.session.get('form_data'))
        else:
            form = ManufacturingCalculatorForm()
    
    rcontext = RequestContext(request, { 'form' : form, 'blueprint': blueprint })
    
    return render_to_response('manufacturing/forms/calculator.haml', rcontext)