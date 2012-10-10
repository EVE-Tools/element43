import mock
import unittest

from functions import calculate_quantity
from eve_db.models import InvBlueprintType

class CalculateQuantityTests(unittest.TestCase):
    def test_calculate_quantity_me_gt_0(self):
        """
        Test 'calculate_quantity' with ME > 0.
        
        Expected result:
        
        material['volume'] = 10.5
        material['quantity'] = 21
        """
        
        form_data = {
            'blueprint_material_efficiency': 10,
            'blueprint_runs': 3,
            'skill_production_efficiency': 5,
            'slot_material_modifier': 0.70
        }
        
        material = { 'quantity': 10, 'volume': 0.5 }
        blueprint = InvBlueprintType(waste_factor=10)
        
        material = calculate_quantity(form_data, blueprint, material)
        
        self.assertEquals(material['quantity'], 21)
        self.assertEquals(material['volume'], 10.5)
    
    def test_calculate_quantity_me_lt_0(self):
        """
        Test 'calculate_quantity' with ME < 0.
        
        Expected result:
        
        material['volume'] = 10.5
        material['quantity'] = 21
        """
        
        form_data = {
            'blueprint_material_efficiency': -10,
            'blueprint_runs': 3,
            'skill_production_efficiency': 5,
            'slot_material_modifier': 0.70
        }
        
        material = { 'quantity': 10, 'volume': 0.5 }
        blueprint = InvBlueprintType(waste_factor=10)
        
        material = calculate_quantity(form_data, blueprint, material)
        
        self.assertEquals(material['quantity'], 54)
        self.assertEquals(material['volume'], 27)