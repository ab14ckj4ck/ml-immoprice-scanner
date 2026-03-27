import unittest
from unittest.mock import patch, mock_open
import numpy as np
from scraper.source1_scraper import (
    fillOptionalData, readSource, buildPageUrls, extractId, 
    extractNewData, getAttr, getLink, getPrice, getRent, 
    getSafetyDeposit, getLivingArea, getEstateSize, getRooms, 
    getPostcode, getCoordinates, getLocationQuality, getPropertyType, 
    getPublished, getHeating, hasFeature, getFeatureNumber, 
    getAccommodations, cleanDuplicates
)
from utils.enums import Listings, Mappings, ScraperValues

class TestSource1Scraper(unittest.TestCase):

    def test_fillOptionalData(self):
        # Setup mock optional data keys
        with patch.object(Mappings, 'OPTIONAL_DATA', ['key1', 'key2']):
            result = {'key1': 10}
            filled = fillOptionalData(result)
            self.assertEqual(filled['key1'], 10)
            self.assertEqual(filled['key2'], 0)

            result_nan = {'key1': np.nan, 'key2': None}
            filled_nan = fillOptionalData(result_nan)
            self.assertEqual(filled_nan['key1'], 0)
            self.assertEqual(filled_nan['key2'], 0)

    @patch("builtins.open", new_callable=mock_open, read_data="http://base.url")
    def test_readSource(self, m):
        self.assertEqual(readSource(), "http://base.url")

    def test_buildPageUrls(self):
        base_links = [{Listings.URL: "http://test.com/", "fin_type": "buy"}]
        with patch.object(ScraperValues, 'STATES', ['state1']):
            urls = buildPageUrls(base_links, pages=1, rows=30)
            self.assertEqual(len(urls), 1)
            self.assertEqual(urls[0][Listings.URL], "http://test.com/state1?rows=30&page=1")
            self.assertEqual(urls[0]['fin_type'], "buy")

    def test_extractId(self):
        self.assertEqual(extractId("http://test.com/listing-12345"), "12345")
        self.assertEqual(extractId("http://test.com/listing-6789/"), "6789")
        self.assertIsNone(extractId("http://test.com/no-id"))

    def test_extractNewData(self):
        html = '<html><script id="__NEXT_DATA__">{"key": "value"}</script></html>'
        self.assertEqual(extractNewData(html), {"key": "value"})
        self.assertIsNone(extractNewData("<html></html>"))

    def test_getAttr(self):
        item = {
            "attributes": {
                "attribute": [
                    {"name": "ATTR1", "values": ["VAL1"]},
                    {"name": "ATTR2", "values": []}
                ]
            }
        }
        self.assertEqual(getAttr(item, "ATTR1"), "VAL1")
        self.assertIsNone(getAttr(item, "ATTR2"))
        self.assertIsNone(getAttr(item, "MISSING"))

    @patch("scraper.source1_scraper.readSource", return_value="http://base.url")
    def test_getLink(self, mock_read):
        item = {"attributes": {"attribute": [{"name": "SEO_URL", "values": ["seo-path"]}]}}
        self.assertEqual(getLink(item), "http://base.url/iad/seo-path")
        self.assertIsNone(getLink({}))

    def test_getPrice(self):
        item = {"attributes": {"attribute": [{"name": "PRICE", "values": ["1250.50"]}]}}
        self.assertEqual(getPrice(item), 1250.5)
        self.assertIsNone(getPrice({}))

    def test_getRent(self):
        item = {"attributes": {"attribute": [{"name": "RENT/PER_MONTH_LETTINGS", "values": ["500"]}]}}
        self.assertEqual(getRent(item), 500.0)

    def test_getSafetyDeposit(self):
        self.assertEqual(getSafetyDeposit({'kaution': '1500'}), 1500.0)
        self.assertIsNone(getSafetyDeposit({'kaution': 'Siehe Preis'}))
        self.assertIsNone(getSafetyDeposit(None))

    def test_getCoordinates(self):
        item = {"attributes": {"attribute": [{"name": "COORDINATES", "values": ["48.1,16.2"]}]}}
        self.assertEqual(getCoordinates(item), (48.1, 16.2))
        self.assertEqual(getCoordinates({}), (None, None))

    def test_getHeating(self):
        item = {'heizung': 'Öl'}
        heating = getHeating(item)
        self.assertEqual(heating[Listings.IS_OIL], 1)
        self.assertEqual(heating[Listings.IS_BIO], 0)

    def test_hasFeature(self):
        item = {'desc': 'Hat einen Balkon'}
        self.assertEqual(hasFeature(item, 'balkon'), 1)
        self.assertEqual(hasFeature(item, 'garten'), 0)

    def test_getFeatureNumber(self):
        self.assertEqual(getFeatureNumber("€ 1.200,50"), 1200.5)
        self.assertEqual(getFeatureNumber(100), 100.0)
        self.assertIsNone(getFeatureNumber("no number"))

    def test_cleanDuplicates(self):
        seen = {"1"}
        buffer = [
            {Listings.ID: "1", Listings.PRICE: 100, Listings.LIVING_AREA: 50}, # seen
            {Listings.ID: "2", Listings.PRICE: None, Listings.LIVING_AREA: 50}, # no price
            {Listings.ID: "3", Listings.PRICE: 100, Listings.LIVING_AREA: None}, # no area
            {Listings.ID: "4", Listings.PRICE: 100, Listings.LIVING_AREA: 50}  # valid
        ]
        cleaned = cleanDuplicates(buffer, seen)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0][Listings.ID], "4")

if __name__ == "__main__":
    unittest.main()
