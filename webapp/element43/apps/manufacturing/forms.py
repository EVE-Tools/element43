from django import forms
from django.contrib.formtools.wizard.views import SessionWizardView
from django.template import RequestContext
from django.shortcuts import render_to_response

from functions import is_valid_blueprint_type_id

from eve_db.models import InvBlueprintType

from apps.manufacturing.help_texts import *

class SelectBlueprintForm(forms.Form):
    blueprint = forms.CharField(max_length=100, help_text=FORM_SELECTBLUEPRINTFORM_BLUEPRINT, widget=forms.TextInput(attrs={ 'class' : 'input-large required' }))
    
    def clean_blueprint(self):
        blueprint_name = self.cleaned_data['blueprint']
        exists = InvBlueprintType.objects.filter(blueprint_type__name=blueprint_name).exists()
        
        if not exists:
            raise forms.ValidationError("Could not find blueprint '%s'" % blueprint_name)
        
        return blueprint_name
        
class ManufacturingCalculatorForm(forms.Form):
    SKILL_INDUSTRY_CHOICES = (
        (0, 0), 
        (1, 1), 
        (2, 2),
        (3, 3),
        (4, 4), 
        (5, 5)
    )
    
    SKILL_PRODUCTION_EFFICIENCY_CHOICES = (
        (0, 0), 
        (1, 1), 
        (2, 2),
        (3, 3),
        (4, 4), 
        (5, 5)
    )
    
    # (typeID, typeName)
    HARDWIRING_CHOICES = (
        (0, "No Hardwiring"),
        (27170, "Zainou 'Beancounter' Industry BX-801"),
        (27167, "Zainou 'Beancounter' Industry BX-802"),
        (27171, "Zainou 'Beancounter' Industry BX-804")
    )
    
    # blueprint related fields
    bpc_material_efficiency = forms.IntegerField(min_value=-4, max_value=1000, initial=0, widget=forms.TextInput(attrs={'class': 'input-mini required'}))
    bpc_production_efficiency = forms.IntegerField(min_value=-4, max_value=1000, initial=0, widget=forms.TextInput(attrs={'class': 'input-mini required'}))
    bpc_runs = forms.IntegerField(min_value=0, max_value=10000, initial=1, widget=forms.TextInput(attrs={'class': 'input-mini required'}))
    bpc_price = forms.DecimalField(min_value=0, max_digits=32, decimal_places=2, initial=0, required=False)
    
    # player skill and item related fields
    skill_industry = forms.ChoiceField(choices=SKILL_INDUSTRY_CHOICES, widget=forms.Select(attrs={'class': 'input-mini required'}))
    skill_production_efficiency = forms.ChoiceField(choices=SKILL_PRODUCTION_EFFICIENCY_CHOICES, widget=forms.Select(attrs={'class': 'input-mini required'}))
    hardwiring = forms.ChoiceField(choices=HARDWIRING_CHOICES, widget=forms.Select(attrs={'class': 'input-xlarge required'}))
    
    # production slot fields
    slot_production_time_modifier = forms.FloatField(min_value=0, max_value=10, initial="1.00", widget=forms.TextInput(attrs={'class': 'input-mini required'}))
    slot_material_modifier = forms.FloatField(min_value=0, max_value=10, initial="1.00", widget=forms.TextInput(attrs={'class': 'input-mini required'}))
    
    # fields for calculating profit
    target_sell_price = forms.DecimalField(min_value=0, max_digits=32, decimal_places=2, initial="0", required=False)