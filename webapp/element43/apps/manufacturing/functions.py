from decimal import Decimal

from django.db import connection

from eve_db.models import InvType, InvBlueprintType, InvTypeMaterial
from apps.market_data.models import ItemRegionStat

def calculate_manufacturing_job(form_data):
    """
    Calculates the manufacturing costs and profits.
    """
    
    # (bp * me waste) + (bp * pe waste) + (bp + slot waste) + bp
    
    data = form_data
    result = {}
    runs = data['bpc_runs']
    blueprint_id = data['blueprint_type_id']
    blueprint = InvBlueprintType.objects.get(blueprint_type__id=blueprint_id)
    
    materials = InvTypeMaterial.objects.values('material_type__name', 'quantity', 'material_type__volume', 'material_type__id').filter(type=blueprint.product_type)
    material_cost_total = 0
    material_volume_total = 0
    
    bpc_me = int(data['bpc_material_efficiency'])
    pe = int(data['skill_production_efficiency'])
    
    waste_multiplier = (blueprint.waste_factor / 100.00)
    
    if bpc_me >= 0:
        waste_multiplier *= float((1 / (bpc_me + 1)))
    else:
        waste_multiplier *= float(1 - bpc_me)
    
    for material in materials:
        stat_object = ItemRegionStat()
        
        try:
            stat_object = ItemRegionStat.objects.get(invtype_id__exact=material['material_type__id'], mapregion_id__exact=10000002)
        except Exception as e:
            stat_object.sellmedian = 0
            connection._rollback()
        
        base_quantity = material['quantity']
        skill_waste = float(((25 - (5 * pe)) * material['quantity'])) / 100
        quantity = int((base_quantity * waste_multiplier) + skill_waste + (base_quantity * data['slot_material_modifier']))
        
        waste = material['quantity'] * waste_multiplier
        material['quantity'] = quantity * runs
        material['price']=stat_object.sellmedian
        material['total']=stat_object.sellmedian*material['quantity']
        material['volume_total']=material['material_type__volume']*material['quantity']
        material_cost_total += material['total']
        material_volume_total += material['volume_total']
    
    result['blueprint'] = blueprint
    result['blueprint_cost_unit'] = data['bpc_price'] / runs
    result['blueprint_cost_total'] = data['bpc_price'] 
    result['materials'] = materials
    result['material_cost_unit'] = material_cost_total / runs
    result['material_cost_total'] = material_cost_total
    result['material_volume_total'] = material_volume_total
    result['revenue_unit'] = data['target_sell_price']
    result['revenue_total'] = data['target_sell_price'] * runs
    result['profit_unit'] = data['target_sell_price'] - Decimal((material_cost_total / runs))
    result['profit_total'] = result['profit_unit'] * runs
    result['blueprint_id'] = blueprint_id
    
    # production time calculation
    IMPLANT_MODIFIER = {
        0: 0.00,
        27170: 0.01,
        27167: 0.02,
        27171: 0.04
    }
    
    industry_skill_level = data['skill_industry']
    production_slot_modifier = data['slot_production_time_modifier']
    implant_modifier = IMPLANT_MODIFIER[int(data['hardwiring'])]
    
    bpc_pe = data['bpc_production_efficiency']
    
    # 1. production time modifier = ptm
    ptm = (1-(0.04 * float(industry_skill_level))) * (1 - implant_modifier) * production_slot_modifier
    
    # 2. production time (pt)
    base_production_time = blueprint.production_time
    productivity_modifier = data['slot_production_time_modifier']
    
    pt = 0
    
    if bpc_pe >= 0:
        pt = base_production_time * (1 - (productivity_modifier/base_production_time) * (bpc_pe / (1 + bpc_pe))) * ptm
    else:
        pt = base_production_time * (1 - (productivity_modifier/base_production_time) * (bpc_pe - 1)) * ptm
    
    result['production_time_unit'] = pt
    result['production_time_total'] = pt * runs
    
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