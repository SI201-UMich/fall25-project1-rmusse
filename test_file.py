import unittest
from Project1 import load_penguin, calculate_average_body_mass_species, calculate_body_flipper_to_mass_ratio, analyze_bill_ratio_mass_relation

class TestAllMethods(unittest.TestCase):

    def setUp(self):
        self.penguins = load_penguin('penguins.csv')


    # TEST ANALYZE BODY MASS - FUNCTION 1
    def test_avg_mass_general_1(self):
        avg_body_mass_dict, heaviest_species_island, highest_avg_mass = calculate_average_body_mass_species(self.penguins)
        self.assertAlmostEqual(avg_body_mass_dict[('Torgersen', 'Adelie')], 3706.37, places=2)
        self.assertFalse(avg_body_mass_dict[('Torgersen', 'Adelie')] == 0)
    
    def test_avg_mass_general_2(self):
        avg_body_mass_dict, heaviest_species_island, highest_avg_mass = calculate_average_body_mass_species(self.penguins)
        self.assertEqual(heaviest_species_island, ('Biscoe', 'Gentoo'))
        self.assertAlmostEqual(highest_avg_mass, 5076.02, places=2)

    def test_avg_mass_edge_case_missing(self):
        penguins_missing = self.penguins + [{'species':'Adelie', 'island':'Torgersen', 'body_mass_g': None}]
        avg_body_mass_dict, heaviest_species_island, highest_avg_mass = calculate_average_body_mass_species(penguins_missing)
        self.assertAlmostEqual(avg_body_mass_dict[('Torgersen', 'Adelie')], 3706.37, places=2)
    
    def test_avg_mass_edge_case_empty_list(self):  
        avg_body_mass_dict, heaviest_species_island, highest_avg_mass = calculate_average_body_mass_species([])
        self.assertEqual(avg_body_mass_dict, {})
        self.assertEqual(heaviest_species_island, None)
        self.assertEqual(highest_avg_mass, 0)
    

    # ##TEST ________ - FUNCTION 2
    def test_flipper_general_1(self):
    # General Test 1 – check that the function returns expected type of result
        avg_body_mass_dict, heaviest_species_island, highest_avg_mass = calculate_average_body_mass_species(self.penguins)
        results_dict = calculate_body_flipper_to_mass_ratio(self.penguins, avg_body_mass_dict)
        adelie_value = results_dict['Adelie']
        self.assertTrue(adelie_value == 'male' or adelie_value == 'female')


    def test_flipper_general_2(self):
    # General Test 2 – check that the result dictionary is not empty
        avg_body_mass_dict, heaviest_species_island, highest_avg_mass = calculate_average_body_mass_species(self.penguins)
        results_dict = calculate_body_flipper_to_mass_ratio(self.penguins, avg_body_mass_dict)
        self.assertFalse(len(results_dict) == 0)


    def test_flipper_edge_1(self):
    # Edge Test 1 – empty penguin list should return an empty dictionary
        results_empty = calculate_body_flipper_to_mass_ratio([], {})
        self.assertEqual(results_empty, {})


    def test_flipper_edge_2(self):
    # Edge Test 2 – missing data should default to 'unknown'
        penguins_missing = [{'species': 'Adelie', 'flipper_length_mm': None, 'sex': None, 'island': 'Biscoe'}]
        results_missing = calculate_body_flipper_to_mass_ratio(penguins_missing, {('Biscoe', 'Adelie'): 3700})
        self.assertEqual(results_missing['Adelie'], 'unknown')




    #TEST ANALYZE BILL RATIO - FUNCTION 3
    def test_bill_mass_general_1(self):
    # General Test 1 – check that the average bill ratio is close to expected
        bill_mass_relation, sex_match = analyze_bill_ratio_mass_relation(
            self.penguins, {('Biscoe', 'Adelie'): 3700}, {'Adelie': 'male'}
        )
        self.assertAlmostEqual(bill_mass_relation[('Biscoe', 'Adelie', 'male')], 2.16, places=2)
        self.assertFalse(bill_mass_relation[('Biscoe', 'Adelie', 'male')] == 0)


    def test_bill_mass_general_2(self):
    # General Test 2 – check that sex_match correctly reflects real data comparison
        bill_mass_relation, sex_match = analyze_bill_ratio_mass_relation(
            self.penguins, {('Biscoe', 'Adelie'): 3700}, {'Adelie': 'male'}
        )
        self.assertEqual(sex_match, True)


    def test_bill_mass_edge_1(self):
    # Edge Test 1 – empty penguin list should give empty results
        result_empty, match_empty = analyze_bill_ratio_mass_relation([], {}, {})
        self.assertEqual(result_empty, {})
        self.assertEqual(match_empty, False)


    def test_bill_mass_edge_2(self):
    # Edge Test 2 – missing data should return empty results and False for sex_match
        penguins_missing = [{'island': 'Biscoe', 'species': 'Adelie', 'sex': None, 'bill_length_mm': None, 'bill_depth_mm': 18.0}]
        result_missing, match_missing = analyze_bill_ratio_mass_relation(penguins_missing, {}, {})
        self.assertEqual(result_missing, {})
        self.assertEqual(match_missing, False)

if __name__ == "__main__":
    unittest.main()