import unittest
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup
from scraper.source1_detail_scraper import (
    readSource, parsePriceInfo, parseEnergy, parseAttributes, detailScraper
)
from utils.enums import ScraperValues

class TestSource1DetailScraper(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="http://test.source")
    def test_readSource(self, m):
        self.assertEqual(readSource(), "http://test.source")

    def test_parsePriceInfo(self):
        # Case 1: Kaution found
        html = "<div>Some text before Kaution: € 1.500,00 some text after</div>"
        soup = BeautifulSoup(html, "html.parser")
        result = parsePriceInfo(soup)
        self.assertEqual(result["kaution"], "1.500,00")

        # Case 2: No Kaution
        html_none = "<div>No info here</div>"
        soup_none = BeautifulSoup(html_none, "html.parser")
        self.assertEqual(parsePriceInfo(soup_none), {})

    def test_parseEnergy(self):
        html = """
        <div data-testid="energy-pass-box">
            <span>hwb 45.5 kwh/m2a klasse b</span>
            <span>fgee 0.9 klasse a</span>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = parseEnergy(soup)
        self.assertEqual(result["hwb"], 45.5)
        self.assertEqual(result["fgee"], 0.9)
        self.assertEqual(result["hwb_class"], ScraperValues.ENERGY_MAP["B"])
        self.assertEqual(result["fgee_class"], ScraperValues.ENERGY_MAP["A"])

        # Test missing box
        soup_empty = BeautifulSoup("<div></div>", "html.parser")
        self.assertEqual(parseEnergy(soup_empty), {})

    def test_parseAttributes(self):
        html = """
        <ul>
            <li data-testid="attribute-item"><span>Zimmer</span><div>3</div></li>
            <li data-testid="attribute-item"><span>Wohnfläche</span><div>80 m²</div></li>
            <li data-testid="attribute-item"><span>Empty</span></li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = parseAttributes(soup)
        self.assertEqual(result["Zimmer"], "3")
        self.assertEqual(result["Wohnfläche"], "80 m²")
        self.assertNotIn("Empty", result)

    @patch("scraper.source1_detail_scraper.fetch")
    @patch("time.sleep")
    def test_detailScraper(self, mock_sleep, mock_fetch):
        # Mock fetch to succeed on second try
        # Use a structure that parseAttributes expects: <li data-testid="attribute-item"><span>Key</span><div>Value</div></li>
        html_content = '<html><li data-testid="attribute-item"><span>Key</span><div>Value</div></li></html>'
        mock_fetch.side_effect = [
            ("Error", 500),
            (html_content, 200)
        ]
        
        result = detailScraper("http://test.url")
        self.assertEqual(result["Key"], "Value")
        self.assertEqual(mock_fetch.call_count, 2)

        # Mock fetch failure (returns None or empty string)
        mock_fetch.side_effect = None
        mock_fetch.return_value = (None, 404)
        result_fail = detailScraper("http://fail.url")
        self.assertEqual(result_fail, {})

if __name__ == "__main__":
    unittest.main()
