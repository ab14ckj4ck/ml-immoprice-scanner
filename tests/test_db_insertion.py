import unittest
from unittest.mock import MagicMock, patch
from database.db_insertion import upsertListings, insertHistory, updateListings, insertFeatures
from utils.enums import Listings, Features

class TestDbInsertion(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cur = MagicMock()

    def test_upsertListings(self):
        listing = {
            Listings.ID: "1",
            Listings.URL: "http://test.com",
            Listings.PRICE: 100000.0,
            Listings.RENT: None,
            Listings.SAFETY_DEPOSIT: 0,
            Listings.LIVING_AREA: 50,
            Listings.ESTATE_SIZE: 100,
            Listings.ROOMS: 2,
            Listings.POSTCODE: "1010",
            Listings.STATE: "wien",
            Listings.LAT: 48.0,
            Listings.LON: 16.0,
            Listings.LOCATION_QUALITY: 1.0,
            Listings.PROPERTY_TYPE: "apartment",
            Listings.FINANCE_TYPE: "buy",
            Listings.PUBLISHED: 123456,
            Listings.SCRAPED_AT: "2023-01-01",
            Listings.HAS_CARPORT: 0,
            Listings.HAS_ELEVATOR: 1,
            Listings.HAS_KITCHEN: 1,
            Listings.HAS_GARAGE: 0,
            Listings.HAS_CELLAR: 1,
            Listings.HAS_PARKING: 0,
            Listings.HAS_CLOSET: 0,
            Listings.HAS_BALCONY: 1,
            Listings.BALCONY_SIZE: 5,
            Listings.HAS_GARDEN: 0,
            Listings.GARDEN_SIZE: 0,
            Listings.HAS_TERRACE: 0,
            Listings.TERRACE_SIZE: 0,
            Listings.HAS_LOGGIA: 0,
            Listings.LOGGIA_SIZE: 0,
            Listings.HAS_WINTERGARDEN: 0,
            Listings.WINTERGARDEN_SIZE: 0,
            Listings.IS_OIL: 0,
            Listings.IS_BIO: 0,
            Listings.IS_ELECTRO: 0,
            Listings.IS_PELLETS: 0,
            Listings.IS_PHOTOVOLTAIK: 0,
            Listings.IS_GEOTHERMAL: 0,
            Listings.IS_AIR_HEATING: 0,
            Listings.IS_FLOOR: 0,
            Listings.IS_CENTRAL: 1,
            Listings.IS_CEILING: 0,
            Listings.IS_OVEN: 0,
            Listings.IS_INFRARED: 0,
            Listings.HWB: 50,
            Listings.HWB_CLASS: 5,
            Listings.FGEE: 0.9,
            Listings.FGEE_CLASS: 7
        }
        
        with patch('database.db_insertion.execute_batch') as mock_exec:
            upsertListings([listing], 20, self.mock_conn, self.mock_cur)
            
            self.assertTrue(mock_exec.called)
            args, kwargs = mock_exec.call_args
            self.assertIn("INSERT INTO listings", args[1])
            self.assertEqual(kwargs['page_size'], 20)

    def test_insertHistory(self):
        listing = {
            Listings.ID: "1",
            Listings.PRICE: 100000.0,
            Listings.RENT: None,
            Listings.SCRAPED_AT: "2023-01-01"
        }
        
        with patch('database.db_insertion.execute_batch') as mock_exec:
            insertHistory([listing], 20, self.mock_cur)
            
            self.assertTrue(mock_exec.called)
            self.assertIn("INSERT INTO history_listings", mock_exec.call_args[0][1])

    def test_insertFeatures(self):
        feature = {
            Features.ID: "1",
            Features.PPM2: 11.5,
            Features.LOG_ESTATE_RATIO: 0.5,
            Features.LOG_DISTANCE_TO_NEAREST_CITY: 1.0,
            Features.LOG_DISTANCE_TO_MAJOR_CITY: 2.0,
            Features.LOG_DISTANCE_TO_TOURISM: 0.5,
            Features.LOG_DISTANCE_TRAIN_STATION: 1.5,
            Features.LOG_COUNT_5KM: 1,
            Features.LOG_COUNT_10KM: 2,
            Features.LOG_COUNT_25KM: 3,
            Features.STATE_VIE: 1,
            Features.STATE_NOE: 0,
            Features.STATE_OOE: 0,
            Features.STATE_SBG: 0,
            Features.STATE_BGL: 0,
            Features.STATE_STK: 0,
            Features.STATE_KTN: 0,
            Features.STATE_TRL: 0,
            Features.STATE_VBG: 0,
            Features.LOG_BALCONY_SIZE: 0,
            Features.LOG_GARDEN_SIZE: 0,
            Features.LOG_TERRACE_SIZE: 0,
            Features.LOG_LOGGIA_SIZE: 0,
            Features.LOG_WINTERGARDEN_SIZE: 0
        }
        
        with patch('database.db_insertion.execute_batch') as mock_exec:
            insertFeatures([feature], 20, self.mock_conn, self.mock_cur)
            
            self.assertTrue(mock_exec.called)
            self.assertIn("INSERT INTO features", mock_exec.call_args[0][1])

if __name__ == '__main__':
    unittest.main()
