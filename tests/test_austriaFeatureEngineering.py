import unittest
import pandas as pd
import numpy as np
from datamanipulation.austriaFeatureEngineering import (
    haversine, quantileElimination, findNearestPointOfInterest, setStates
)
from utils.enums import Listings, Features

class TestAustriaFeatureEngineering(unittest.TestCase):

    def test_haversine(self):
        # Distance between Vienna (48.2082, 16.3738) and Graz (47.0707, 15.4395) is approx 145 km
        dist = haversine(48.2082, 16.3738, 47.0707, 15.4395)
        self.assertTrue(140 < dist < 150)

    def test_quantileElimination(self):
        df = pd.DataFrame({Listings.PRICE: range(100)})
        cleaned = quantileElimination(df, Listings.PRICE, 0.05, 0.95)
        self.assertLess(len(cleaned), 100)
        self.assertTrue(cleaned[Listings.PRICE].min() >= 4) # 5th percentile of 0..99 is ~4.95

    def test_findNearestPointOfInterest(self):
        df = pd.DataFrame({
            Listings.LAT: [48.2082, 47.0707],
            Listings.LON: [16.3738, 15.4395]
        })
        # POI at Vienna
        pois = [{Listings.LAT: 48.2082, Listings.LON: 16.3738}]
        
        min_dist, c5, c10, c25 = findNearestPointOfInterest(df, pois)
        
        self.assertEqual(min_dist[0], 0.0)
        self.assertTrue(min_dist[1] > 140)
        self.assertEqual(c5[0], 1)
        self.assertEqual(c5[1], 0)
        self.assertEqual(c25[0], 1)
        self.assertEqual(c25[1], 0)

    def test_setStates(self):
        df = pd.DataFrame({
            Listings.STATE: ['kaernten', 'wien', 'niederoesterreich']
        })
        df_features = pd.DataFrame()
        
        result = setStates(df, df_features)
        
        # KT=kaernten, VIE=wien, NOE=niederoesterreich
        self.assertEqual(result[Features.STATE_KTN].iloc[0], 1)
        self.assertEqual(result[Features.STATE_KTN].iloc[1], 0)
        self.assertEqual(result[Features.STATE_VIE].iloc[1], 1)
        self.assertEqual(result[Features.STATE_VIE].iloc[0], 0)
        self.assertEqual(result[Features.STATE_NOE].iloc[2], 1)

if __name__ == '__main__':
    unittest.main()
