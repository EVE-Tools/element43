import math

from decimal import Decimal

from django.db import connection

# App settings
from apps.manufacturing.settings import MANUFACTURING_MAX_BLUEPRINT_HISTORY, MANUFACTURING_BLUEPRINT_HISTORY_SESSION

# Models
from eve_db.models import InvBlueprintType, InvTypeMaterial, RamTypeRequirement
from apps.market_data.models import ItemRegionStat

def is_producible(type_id):
    """
    Returns 'True' if the given type_id can be built with an Blueprint and 'False' otherwise.
    """
    return InvBlueprintType.objects.filter(product_type__id=type_id).exists()

def is_tech1(type_id):
    """
    Returns 'True' if the given type_id belongs to a Tech I item and 'False' otherwise.
    """
    return InvBlueprintType.objects.filter(product_type__id=type_id, tech_level=1).exists()


def is_advanced_manufacturing(blueprint):
    """
    Returns 'True' if the given blueprints requires more advanced production calculations.
    Normally those are all blueprints of items > Tech I
    """
    return RamTypeRequirement.objects.filter(type=blueprint).exists()


def calculate_quantities(form_data, blueprint, materials):
    """
    Returns the the given materials dictionary with the calculated quantities for all items.
    The quantity of a material depends on:

    - Blueprint base waste
    - Blueprint material level (ME)
    - Skill waste (Production efficiency)
    - Manufacturing installation material multiplier)
    """
    for material in materials:
        material = calculate_quantity(form_data, blueprint, material)

    return materials


def calculate_quantity(form_data, blueprint, material):
    """
    Returns the the given material with the calculated quantities for this material.
    The quantity of a material depends on:

    - Blueprint base waste
    - Blueprint material level (ME)
    - Skill waste (Production efficiency)
    - Manufacturing installation material multiplier)
    """
    blueprint_me = int(form_data['blueprint_material_efficiency'])
    blueprint_runs = int(form_data['blueprint_runs'])
    skill_production_efficiency = int(form_data['skill_production_efficiency'])

    base_waste_multiplier = float(blueprint.waste_factor) / 100

    if blueprint_me >= 0:
        base_waste_multiplier *= (float(1) / float((blueprint_me + 1)))
    else:
        base_waste_multiplier *= float(1 - blueprint_me)

    base_quantity = material['quantity']
    base_waste = base_quantity * base_waste_multiplier
    skill_waste = float(((25 - (5 * skill_production_efficiency)) * base_quantity)) / 100
    quantity_unit = (base_quantity * form_data['slot_material_modifier']) + base_waste + skill_waste
    quantity_total = round(quantity_unit) * blueprint_runs

    material['quantity'] = int(quantity_total)
    material['volume'] = material['quantity'] * material['volume']

    return material


def calculate_material_prices(materials):
    """
    Returns the given materials dictionary with calculated prices.

    Beware: The prices are 'sell median' from 'The Forge' region.
    """
    try:
        # Build the list of material ids for which the price has to be fetched
        material_ids = [material['id'] for material in materials]
        materials_prices = ItemRegionStat.objects.values('invtype__id', 'sell_95_percentile').filter(invtype_id__in=material_ids,
                                                                                             mapregion_id__exact=10000002)

        for material_price in materials_prices:
            for material in materials:
                if material['id'] == material_price['invtype__id']:
                    material['price'] = material_price['sell_95_percentile']
                    material['price_total'] = material_price['sell_95_percentile'] * material['quantity']

    except Exception:
        connection._rollback()

    return materials

def get_materials(form_data, blueprint):
    """
    Returns the amount of materials required for manufacturing the given blueprint.
    """
    if is_advanced_manufacturing(blueprint):
        materials = get_tech2_materials(form_data, blueprint)
    else:
        materials = get_tech1_materials(form_data, blueprint)
    
    return materials

def get_tech1_materials(form_data, blueprint):
    """
    Returns the bill of materials for a Tech I blueprint.
    The bill of materials already contains prices but they are not calculated yet.
    If you want to get prices for the materials in the bill of materials you have
    to pass the result of this function to 'calculate_material_prices'!
    """
    materials = []
    base_materials = InvTypeMaterial.objects.values('material_type__id',
                                                    'material_type__name',
                                                    'material_type__volume',
                                                    'quantity').filter(type=blueprint.product_type)

    for base_material in base_materials:
        materials.append(dict({
            'id': base_material['material_type__id'],
            'name': base_material['material_type__name'],
            'quantity': base_material['quantity'],
            'volume': base_material['material_type__volume'],
            'price': 0,
            'price_total': 0,
            'producible': is_producible(base_material['material_type__id'])
        }))

    materials = calculate_quantities(form_data, blueprint, materials)

    return materials


def get_tech2_materials(form_data, blueprint):
    """
    Returns the bill of materials for a Tech II blueprint.
    The bill of materials already contains prices but they are not calculated yet.
    If you want to get prices for the materials in the bill of materials you have
    to pass the result of this function to 'calculate_material_prices'!
    """

    materials = []  # bill of materials

    """
    Calculating the bill of materials for a Tech II blueprint is a bit tricky. Most
    Tech II blueprints require a Tech I item and additional materials to manufacture
    the Tech II item.

    Target Painter II for example requires Target Painter I. One of the exceptions
    to that rule are Tech II rigs. They don't require their Tech I variant.

    To calculate the bill of materials three things have to be considered:

    1. Materials needed for the Tech I item (tech1_item_materials)
    2. Materials needed for the Tech II item (tech2_item_materials)
    3. Build requirements for the Tech II item (build_requirements)

    materials = (tech2_item_materials - tech1_item_materials) + build_requirements

    The bill of materials for the Tech II includes the materials required to manufacture
    the Tech I item. Therefor the bill of materials for Tech I item have to be
    subtracted to get a list of materials that are exclusively needed for the
    Tech II item.
    """

    blueprint_runs = int(form_data['blueprint_runs'])
    tech1_item_materials = []

    # Find build requirements for the Tech II item (does contain the Tech I item if required)
    build_requirements = RamTypeRequirement.objects.values('required_type__id',
                                                           'required_type__name',
                                                           'required_type__volume',
                                                           'quantity', 'recycle').filter(type__id=blueprint.blueprint_type.id,
                                                                                         activity_type__id=1).exclude(required_type__group__category__id=16)

    for build_requirement in build_requirements:
        materials.append(dict({
            'id': build_requirement['required_type__id'],
            'name': build_requirement['required_type__name'],
            'quantity': build_requirement['quantity'] * blueprint_runs,
            'volume': build_requirement['required_type__volume'] * build_requirement['quantity'] * blueprint_runs,
            'price': 0,
            'price_total': 0,
            'producible':is_producible(build_requirement['required_type__id'])
        }))

        # If recycle is True the build_requirement is the required Tech I item.
        if build_requirement['recycle'] == True and is_tech1(build_requirement['required_type__id']):

            tech1_item_materials = InvTypeMaterial.objects.values('material_type__id',
                                                                  'material_type__name',
                                                                  'material_type__volume',
                                                                  'quantity').filter(type=build_requirement['required_type__id'])

    # Get the bill of materials for the Tech II item
    extra_materials = InvTypeMaterial.objects.values('material_type__id',
                                                     'material_type__name',
                                                     'material_type__volume',
                                                     'quantity').filter(type=blueprint.product_type)

    for extra_material in extra_materials:
        # If on of the materials from the bill of materials of the Tech II item is
        # found in the bill of materials for the Tech I item substract them.
        for tech1_item_material in tech1_item_materials:
            if tech1_item_material['material_type__id'] == extra_material['material_type__id']:
                extra_material['quantity'] -= tech1_item_material['quantity']

        # Only if the quantity of the material is greater 0 after the substraction add the
        # material to the bill of materials.
        if extra_material['quantity'] > 0:
            mat = {
                'id': extra_material['material_type__id'],
                'name': extra_material['material_type__name'],
                'quantity': extra_material['quantity'],
                'volume': extra_material['material_type__volume'],
                'price': 0,
                'price_total': 0,
                'producible':is_producible(extra_material['material_type__id'])
            }

            mat = calculate_quantity(form_data, blueprint, mat)
            materials.append(mat)

    return materials

def calculate_production_time(form_data, blueprint):
    """ Returns the production time for the given blueprint. """
    
    """
    The following data is taken into account while calculation:
    
    1. Players industry skill level
    2. Players hardwirings
    3. Installation slot production time modifier
    4. Blueprint Production efficiency
    """
    # implant modifiers. (type_id, modifier)
    IMPLANT_MODIFIER = {
        0: 0.00,  # no hardwiring
        27170: 0.01,  # Zainou 'Beancounter' Industry BX-801
        27167: 0.02,  # Zainou 'Beancounter' Industry BX-802
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
        production_time *= (1 - (float(blueprint.productivity_modifier) / base_production_time) * (blueprint_pe - 1))
    
    return production_time

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

    result = {}  # result dictionary which will be returned
    blueprint_type_id = int(form_data['blueprint_type_id'])
    blueprint_runs = int(form_data['blueprint_runs'])
    blueprint = InvBlueprintType.objects.select_related().get(blueprint_type__id=blueprint_type_id)
    result['produced_units'] = blueprint.product_type.portion_size * blueprint_runs

    # --------------------------------------------------------------------------
    # Calculate bill of materials
    # --------------------------------------------------------------------------
    materials = get_materials(form_data, blueprint)
    materials = calculate_material_prices(materials)
    materials_cost_total = math.fsum([material['price_total'] for material in materials])
    materials_volume_total = math.fsum([material['volume'] for material in materials])

    # sort materials by name:
    materials.sort(key=lambda material: material['name'])

    result['materials'] = materials
    result['materials_cost_unit'] = materials_cost_total / result['produced_units']
    result['materials_cost_total'] = materials_cost_total
    result['materials_volume_total'] = materials_volume_total

    # --------------------------------------------------------------------------
    # Calculate production time
    # --------------------------------------------------------------------------
    production_time = calculate_production_time(form_data, blueprint)

    result['production_time_run'] = round(production_time)
    result['production_time_total'] = round(production_time * blueprint_runs)

    # add all the other values to the result dictionary
    result['blueprint_cost_unit'] = form_data['blueprint_price'] / result['produced_units']
    result['blueprint_cost_total'] = form_data['blueprint_price']
    result['revenue_unit'] = form_data['target_sell_price']
    result['revenue_total'] = form_data['target_sell_price'] * result['produced_units']
    result['total_cost_unit'] = result['blueprint_cost_unit'] + Decimal((materials_cost_total / result['produced_units']))
    result['total_cost_total'] = result['total_cost_unit'] * result['produced_units']
    result['profit_unit'] = form_data['target_sell_price'] - result['total_cost_unit']
    result['profit_total'] = result['profit_unit'] * result['produced_units']
    result['profit_total_hour'] = result['profit_total'] / Decimal(result['production_time_total'] / 3600)
    result['profit_total_day'] = result['profit_total_hour'] * 24
    
    if result['profit_total'] > 0 and result['total_cost_total'] > 0:
        result['profit_total_percent'] = (result['profit_total'] / result['total_cost_total']) * 100
    else:
        result['profit_total_percent'] = 0
    print "result['profit_total_percent']: ", result['profit_total_percent']
        
    result['blueprint_type_id'] = blueprint_type_id
    result['blueprint_name'] = blueprint.blueprint_type.name
    result['blueprint_runs'] = blueprint_runs
    
    brokers_fee = form_data.get('brokers_fee', 0)
    sales_tax = form_data.get('sales_tax', 0)
    
    if not brokers_fee:
        brokers_fee = 0
        
    if not sales_tax:
        sales_tax = 0
    
    result['brokers_fee_unit'] = result['revenue_unit'] * (brokers_fee / 100)
    result['brokers_fee_total'] = result['brokers_fee_unit'] * result['produced_units']
    result['sales_tax_unit'] = result['revenue_unit'] * (sales_tax / 100)
    result['sales_tax_total'] = result['sales_tax_unit'] * result['produced_units']
    result['profit_unit'] = form_data['target_sell_price'] - result['total_cost_unit'] - result['sales_tax_unit'] - result['brokers_fee_unit']
    result['profit_total'] = result['profit_unit'] * result['produced_units']

    return result


def update_blueprint_history(request, blueprint):
    """
    Adds the given blueprint to the blueprint history (which is part of the session in the request).
    """
    history = request.session.get(MANUFACTURING_BLUEPRINT_HISTORY_SESSION, [])
    add_entry = True

    # Don't add the blueprint if it is already in there.
    for entry in history:
        if entry['id'] == blueprint.blueprint_type.id:
            add_entry = False
            break

    if add_entry:
        if len(history) == MANUFACTURING_MAX_BLUEPRINT_HISTORY:
            # delete the last element of the history which is the oldest
            del history[-1]

        # insert the latest blueprint at the beginning of the list
        history.insert(0, {'id': blueprint.blueprint_type.id, 'name': blueprint.blueprint_type.name})

    request.session[MANUFACTURING_BLUEPRINT_HISTORY_SESSION] = history
