from django.test import TestCase

from apps.manufacturing.functions import calculate_manufacturing_job

class ManufacturingCalculationAmarrFuelBlockTest(TestCase):
    fixtures = ['amarrfuelblock.json', 'materials.json']
    
    def setUp(self):
        self.form_data = {
            'blueprint_type_id': 4315,
            'blueprint_runs': 300,
            'blueprint_material_efficiency': 1000,
            'blueprint_production_efficiency': 1000,
            'skill_production_efficiency': 5,
            'slot_material_modifier': 1.00,
            'hardwiring': 0,
            'slot_production_time_modifier': 1.00,
            'skill_industry': 5,
            'blueprint_price': 2000000,
            'target_sell_price': 12700
        }
    
    def test_production_time(self):
        """
        Check production time
        
        Equations:
         
        production_time_modifier = (1 - (0.04 * industry_skill)) * (1 - implant_modifier) * production_slot_modifier
        production_time = base_production_time * (1 - (productivity_level / base_production_time) * (PE / (1 + PE))) * production_time_modifier
        
        Based on those equations and the values from the form_data dictionary:
        
        production_time_modifier = (1 - (0.04 * 5)) * (1 - 0) * 1.0 = 0.8
        production_time = 300 * (1 - (120 / 300) * (1000 / (1 + 1000))) * 0.8 = 144.0959040959041 (seconds)
        """
        result = calculate_manufacturing_job(self.form_data)
        self.assertEquals(result['production_time_run'], 144.0959040959041)
        self.assertEquals(result['production_time_total'], round(144.0959040959041*300)) # 300 runs
    
    def test_materials(self):
        result = calculate_manufacturing_job(self.form_data)
        print result['materials']