import unittest
from vessel_calc import k_value_calculation
from vessel_calc import vertical_vessel_min_diameter
from vessel_calc import demister_dimensions
from vessel_calc import choose_bottom_to_LSAL_for_vertical_sep
from vessel_calc import calc_bottom_volume_for_vertical_sep
from vessel_calc import calc_liquid_zone_for_vertical_vessel

class MyTestCase(unittest.TestCase):
    def test_k_value_calculation1(self):
        k_value = k_value_calculation(0.008, 'N', 7.67, 594.7, 19.7)
        self.assertAlmostEqual(k_value,
                         0.038, 4, 'Check answer closely: might be acceptable')  # add assertion here

    def test_k_value_calculation2(self):
        k_value = k_value_calculation(0.008, 'Y', 7.67, 594.7, 19.7)
        self.assertAlmostEqual(k_value,
                         0.08, 4, 'Check answer closely: might be acceptable')  # add assertion here

    def test_k_value_calculation3(self):
        k_value = k_value_calculation(0.001, 'N', 15, 645, 8)
        self.assertAlmostEqual(k_value,
                         0.022, 3, 'Check answer closely: might be acceptable')  # add assertion here

    def test_vertical_vessel_min_diameter(self):
        min_diameter = vertical_vessel_min_diameter(0.038, 594.7, 19.7, 1, 30596)
        self.assertAlmostEqual(min_diameter, 1.635, 2, 'Check answer closely: might be acceptable')

    def test_demister_dimensions(self):
        demister_diameter = demister_dimensions(0.12, 691.29, 13.29, 1, 52998)
        self.assertAlmostEqual(demister_diameter, 1.283, 3, 'Check answer closely: might be acceptable')

    def test_h_0_E(self):
        h_0 = choose_bottom_to_LSAL_for_vertical_sep('E', 1.575)
        self.assertAlmostEqual(h_0, 0.5, 3, 'Check answer closely: might be acceptable')

    def test_h_0_S(self):
        h_0 = choose_bottom_to_LSAL_for_vertical_sep('S', 1.575)
        self.assertAlmostEqual(h_0, -0.394, 3, 'Check answer closely: might be acceptable')

    def test_bot_volume_for_vert_sep_E(self):
        bot_vol = calc_bottom_volume_for_vertical_sep('E', 1.575, 0.5)
        self.assertAlmostEqual(bot_vol, 1.485, 2, 'Check answer closely: might be acceptable')

    def test_bot_volume_for_vert_sep_S(self):
        bot_vol = calc_bottom_volume_for_vertical_sep('S', 1.575, -0.394)
        self.assertAlmostEqual(bot_vol, 0.367, 3, 'Check answer closely: might be acceptable')

    def test_calc_liquid_zone_for_vertical_sep_zone_1(self):
        zone_height = calc_liquid_zone_for_vertical_vessel(120, 1.575, 1, 2650, 691, 'E')
        self.assertAlmostEqual(zone_height, 0.066, 3, 'Check answer closely: might be acceptable')

    def test_calc_liquid_zone_for_vertical_sep_zone_2(self):
        zone_height = calc_liquid_zone_for_vertical_vessel(120, 1.575, 2, 2650, 691, 'E')
        self.assertAlmostEqual(zone_height, 0.066, 3, 'Check answer closely: might be acceptable')

    def test_calc_liquid_zone_for_vertical_sep_zone_3(self):
        zone_height = calc_liquid_zone_for_vertical_vessel(120, 1.575, 3, 2650, 691, 'E')
        self.assertAlmostEqual(zone_height, 0.066, 3, 'Check answer closely: might be acceptable')

if __name__ == '__main__':
    unittest.main()
