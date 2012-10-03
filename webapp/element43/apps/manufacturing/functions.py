from decimal import Decimal

from django.db import connection

from eve_db.models import InvType, InvBlueprintType, InvTypeMaterial
from apps.market_data.models import ItemRegionStat

def calculate_manufacturing_job(form_data):
    """
    Calculates the manufacturing costs and profits.
    """
    
    #
    # This method is basically divided in two sections:
    #
    # 1. Calculate bill of materials
    # 2. Calculate production time
    #
    
    # initialize the result dictionary which will be returned
    result = {}
    
    # --------------------------------------------------------------------------
    # Calculate bill of materials
    # --------------------------------------------------------------------------
    blueprint_type_id = int(form_data['blueprint_type_id'])
    blueprint_runs = int(form_data['blueprint_runs'])
    blueprint_me = int(form_data['blueprint_material_efficiency'])
    blueprint = InvBlueprintType.objects.get(blueprint_type__id=blueprint_type_id)
    materials = InvTypeMaterial.objects.values('material_type__name', 'quantity', 'material_type__volume', 'material_type__id').filter(type=blueprint.product_type)
    materials_cost_total = 0
    materials_volume_total = 0
    base_waste_multiplier = float(blueprint.waste_factor) / 100
    
    if blueprint_me >= 0:
        base_waste_multiplier *= float((1 / (blueprint_me + 1)))
    else:
        base_waste_multiplier *= float(1 - blueprint_me)
    
    for material in materials:
        # get the region stat object for the material in the Forge region
        stat_object = ItemRegionStat()
        
        try:
            stat_object = ItemRegionStat.objects.get(invtype_id__exact=material['material_type__id'], mapregion_id__exact=10000002)
        except Exception as e:
            stat_object.sellmedian = 0
            connection._rollback()
            
        base_quantity = material['quantity']
        
        # first: calculate base waste
        base_waste = base_quantity * base_waste_multiplier
        
        # second: calculate skill waste
        skill_production_efficiency = int(form_data['skill_production_efficiency'])
        skill_waste = float(((25 - (5 * skill_production_efficiency)) * base_quantity)) / 100
        
        # third: calculate the amount of materials needed depending on th installation slot material modifier and add the waste
        quantity_unit = (base_quantity * form_data['slot_material_modifier']) + base_waste + skill_waste
        quantity_total = round(quantity_unit * blueprint_runs)
        
        material['quantity'] = int(quantity_total)
        material['price'] = stat_object.sellmedian
        material['total'] = stat_object.sellmedian * quantity_total
        material['volume_total'] = material['material_type__volume'] * quantity_total
        materials_cost_total += material['total']
        materials_volume_total += material['volume_total']
    
    result['materials'] = materials
    result['materials_cost_unit'] = materials_cost_total / blueprint_runs
    result['materials_cost_total'] = materials_cost_total
    result['materials_volume_total'] = materials_volume_total
    
    # --------------------------------------------------------------------------
    # Calculate production time
    # --------------------------------------------------------------------------
    
    # implant modifiers. (type_id, modifier)
    IMPLANT_MODIFIER = {
        0: 0.00, # no hardwiring
        27170: 0.01, # Zainou 'Beancounter' Industry BX-801
        27167: 0.02, # Zainou 'Beancounter' Industry BX-802
        27171: 0.04  # Zainou 'Beancounter' Industry BX-804
    }
    
    # calculate production time modifuer
    implant_modifier = IMPLANT_MODIFIER[int(form_data['hardwiring'])]
    slot_productivity_modifier = form_data['slot_production_time_modifier']
    production_time_modifier = (1 - (0.04 * float(form_data['skill_industry']))) * (1 - implant_modifier) * slot_productivity_modifier
    
    base_production_time = blueprint.production_time
    production_time = base_production_time * production_time_modifier
    blueprint_pe = form_data['blueprint_production_efficiency']
    
    if blueprint_pe >= 0:
        production_time *= (1 - (float(blueprint.productivity_modifier) / base_production_time) * (blueprint_pe / (1.00 + blueprint_pe)))
    else:
        production_time *= (1 - (blueprint.productivity_modifier / base_production_time) * (blueprint_pe - 1))
    
    result['production_time_unit'] = production_time
    result['production_time_total'] = production_time * blueprint_runs
    
    # add all the other values to the result dictionary
    product = InvType.objects.get(pk=blueprint.product_type.id)
    result['produced_units'] = product.portion_size * blueprint_runs
    result['blueprint_cost_unit'] = form_data['blueprint_price'] / result['produced_units']
    result['blueprint_cost_total'] = form_data['blueprint_price']
    result['revenue_unit'] = form_data['target_sell_price']
    result['revenue_total'] = form_data['target_sell_price'] * blueprint_runs
    result['total_cost_unit'] = result['blueprint_cost_unit'] + Decimal((materials_cost_total / result['produced_units']))
    result['total_cost_total'] = result['total_cost_unit'] * result['produced_units']
    result['profit_unit'] = form_data['target_sell_price'] - result['total_cost_unit']
    result['profit_total'] = result['profit_unit'] * blueprint_runs
    result['blueprint_type_id'] = blueprint_type_id
    result['blueprint_runs'] = blueprint_runs
    
    return result

def is_valid_blueprint_type_id(blueprint_type_id):
    """
    Validates that the given blueprint_type_id is a valid type id.
    
    Valid means:
    * must be a number (so it can be casted to an integer)
    * the type id must be in the database 
    """
    
    # try to cast the argument to int. if this fails blueprint_type_id is not a number.
    try:
        blueprint_type_id = int(blueprint_type_id)
    except ValueError:
        return False
    
    # lookup the blueprint type id in the database and return True or False
    return InvBlueprintType.objects.filter(pk=blueprint_type_id).exists()