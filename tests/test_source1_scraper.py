import unittest
import numpy as np
from scraper.source1_scraper import (
    fillOptionalData, getAttr, getPrice, getRent, getSafetyDeposit,
    getLivingArea, getEstateSize, getRooms, getCoordinates,
    getHeating, hasFeature, getFeatureNumber, getAccommodations,
    OPTIONAL_DATA
)

class TestSource1Scraper(unittest.TestCase):

    def test_fillOptionalData(self):
        input_data = {"existing": 1}
        result = fillOptionalData(input_data)
        for key in OPTIONAL_DATA:
            self.assertIn(key, result)
            self.assertEqual(result[key], 0)
        
        input_nan = {"has_garage": np.nan}
        result_nan = fillOptionalData(input_nan)
        self.assertEqual(result_nan["has_garage"], 0)

    def test_getAttr(self):
        item = {
            "attributes": {
                "attribute": [
                    {"name": "TEST_ATTR", "values": ["Test Value"]},
                    {"name": "OTHER", "values": ["123"]}
                ]
            }
        }
        self.assertEqual(getAttr(item, "TEST_ATTR"), "Test Value")
        self.assertIsNone(getAttr(item, "MISSING"))
        self.assertIsNone(getAttr({}, "TEST_ATTR"))

    def test_getPrice(self):
        item = {"attributes": {"attribute": [{"name": "PRICE", "values": ["123000"]}]}}
        self.assertEqual(getPrice(item), 123000.0)
        
        item_invalid = {"attributes": {"attribute": [{"name": "PRICE", "values": ["invalid"]}]}}
        self.assertIsNone(getPrice(item_invalid))

    def test_getRent(self):
        item = {"attributes": {"attribute": [{"name": "RENT/PER_MONTH_LETTINGS", "values": ["500.50"]}]}}
        self.assertEqual(getRent(item), 500.50)

    def test_getSafetyDeposit(self):
        item = {"kaution": "1200"}
        self.assertEqual(getSafetyDeposit(item), 1200.0)
        
        item_text = {"kaution": "€ 3.000,00"}
        self.assertEqual(getSafetyDeposit(item_text), 3000.0)
        
        item_see_price = {"kaution": "Siehe Preis"}
        self.assertIsNone(getSafetyDeposit(item_see_price))

    def test_getLivingArea(self):
        item = {"attributes": {"attribute": [{"name": "ESTATE_SIZE/LIVING_AREA", "values": ["85"]}]}}
        self.assertEqual(getLivingArea(item), 85.0)

    def test_getEstateSize(self):
        item = {"attributes": {"attribute": [{"name": "ESTATE_SIZE", "values": ["500"]}]}}
        self.assertEqual(getEstateSize(item), 500.0)

    def test_getRooms(self):
        item = {"attributes": {"attribute": [{"name": "NUMBER_OF_ROOMS", "values": ["3"]}]}}
        self.assertEqual(getRooms(item), 3)
        
        item_zero = {"attributes": {"attribute": [{"name": "NUMBER_OF_ROOMS", "values": ["0"]}]}}
        self.assertIsNone(getRooms(item_zero))

    def test_getCoordinates(self):
        item = {"attributes": {"attribute": [{"name": "COORDINATES", "values": ["48.2082,16.3738"]}]}}
        lat, lon = getCoordinates(item)
        self.assertEqual(lat, 48.2082)
        self.assertEqual(lon, 16.3738)
        
        item_none = {}
        self.assertEqual(getCoordinates(item_none), (None, None))

    def test_getHeating(self):
        item = {"heizung": "Öl, hauszentralheizung"}
        heating = getHeating(item)
        self.assertEqual(heating["oil"], 1)
        self.assertEqual(heating["central_heating"], 1)
        
        # Check a specific one from the list that should be 0
        self.assertEqual(heating["floor_heating"], 0)
        
        item2 = {"heizung": "Fußbodenheizung"}
        self.assertEqual(getHeating(item2)["floor_heating"], 1)

    def test_hasFeature(self):
        # hasFeature checks if key is in item keys OR in values string
        self.assertEqual(hasFeature({"balkon": "ja"}, "balkon"), 1)
        self.assertEqual(hasFeature({"feature": "mit balkon"}, "balkon"), 1)
        self.assertEqual(hasFeature({"feature": "kein garten"}, "garage"), 0)

    def test_getFeatureNumber(self):
        self.assertEqual(getFeatureNumber(100), 100.0)
        self.assertEqual(getFeatureNumber("100"), 100.0)
        self.assertEqual(getFeatureNumber("€ 1.200,50"), 1200.50)
        self.assertIsNone(getFeatureNumber(None))

    def test_getAccommodations(self):
        item = {
            "balkon": "10 m²",
            "garage": "Ja"
        }
        acc = getAccommodations(item)
        self.assertEqual(acc["has_balcony"], 1)
        self.assertEqual(acc["balcony_size"], 10.0)
        self.assertEqual(acc["has_garage"], 1)
        self.assertEqual(acc["has_garden"], 0)

if __name__ == '__main__':
    unittest.main()
