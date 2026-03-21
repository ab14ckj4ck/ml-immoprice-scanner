import unittest
import pandas as pd
import numpy as np
from datamanipulation.cleanData import (
    quantileElimination, minMax, getLogNorm, getRatio,
    haversine, setHousingType
)

class TestCleanData(unittest.TestCase):
    
    def test_quantileElimination(self):
        df = pd.DataFrame({'val': range(100)})
        # 0..99. 5th percentile is ~5, 95th is ~94
        cleaned = quantileElimination(df, 'val', 0.05, 0.95)
        # Check that we removed some data
        self.assertLess(len(cleaned), 100)
        # Check boundaries roughly
        self.assertTrue(cleaned['val'].min() >= 4)
        self.assertTrue(cleaned['val'].max() <= 95)

    def test_minMax(self):
        df = pd.DataFrame({'val': [10, 20, 30]})
        normalized = minMax(df, 'val')
        self.assertIn('norm_val', normalized.columns)
        self.assertEqual(normalized['norm_val'].iloc[0], 0.0)
        self.assertEqual(normalized['norm_val'].iloc[2], 1.0)
        self.assertEqual(normalized['norm_val'].iloc[1], 0.5)

        # Test constant column
        df_const = pd.DataFrame({'val': [10, 10]})
        norm_const = minMax(df_const, 'val')
        self.assertEqual(norm_const['norm_val'].iloc[0], 0)

    def test_getLogNorm(self):
        df = pd.DataFrame({'val': [1, np.e, 10]})
        logged = getLogNorm(df, 'val')
        self.assertAlmostEqual(logged['log_val'].iloc[0], 0.0)
        self.assertAlmostEqual(logged['log_val'].iloc[1], 1.0)
        
        # Test 0 or negative
        df_neg = pd.DataFrame({'val': [0, -1, 1]})
        logged_neg = getLogNorm(df_neg, 'val')
        self.assertTrue(np.isnan(logged_neg['log_val'].iloc[0]))
        self.assertTrue(np.isnan(logged_neg['log_val'].iloc[1]))

    def test_getRatio(self):
        df = pd.DataFrame({
            'a': [10, 20, 30],
            'b': [2, 0, 5]
        })
        ratioed = getRatio(df, 'a', 'b', 'ratio')
        self.assertEqual(ratioed['ratio'].iloc[0], 5.0)
        self.assertTrue(np.isnan(ratioed['ratio'].iloc[1])) # Div by zero replacement
        self.assertEqual(ratioed['ratio'].iloc[2], 6.0)

    def test_haversine(self):
        # Distance between Vienna (48.2082, 16.3738) and Graz (47.0707, 15.4395) is approx 145 km
        dist = haversine(48.2082, 16.3738, 47.0707, 15.4395)
        self.assertTrue(140 < dist < 150)
        
        # Distance to self is 0
        self.assertEqual(haversine(0, 0, 0, 0), 0)

    def test_setHousingType(self):
        df = pd.DataFrame({'property_type': ['A', 'B', 'C', 'D']})
        APARTMENT_TYPES = ['A', 'B']
        HOUSE_TYPES = ['C']
        
        typed = setHousingType(df, APARTMENT_TYPES, HOUSE_TYPES)
        
        self.assertEqual(typed['is_apartment'].iloc[0], 1)
        self.assertEqual(typed['is_apartment'].iloc[2], 0)
        self.assertEqual(typed['is_house'].iloc[2], 1)
        self.assertEqual(typed['is_house'].iloc[0], 0)
        self.assertEqual(typed['is_house'].iloc[3], 0)

if __name__ == '__main__':
    unittest.main()
