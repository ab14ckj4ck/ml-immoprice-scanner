import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from scraper.source1_detail_scraper import (
    parsePriceInfo, parseEnergy, parseAttributes, detailScraper, ENERGY_MAP
)

class TestSource1DetailScraper(unittest.TestCase):

    def test_parsePriceInfo(self):
        # Case 1: Kaution present
        html = "<div>Some text Kaution: € 1.200,00 more text</div>"
        soup = BeautifulSoup(html, "html.parser")
        data = parsePriceInfo(soup)
        self.assertEqual(data.get("kaution"), "1.200,00")

        # Case 2: No Kaution
        html_no_kaution = "<div>No deposit mentioned</div>"
        soup_no = BeautifulSoup(html_no_kaution, "html.parser")
        self.assertEqual(parsePriceInfo(soup_no), {})
        
        # Case 3: Kaution format variation
        html_var = "<div>Kaution: 3000</div>"
        soup_var = BeautifulSoup(html_var, "html.parser")
        self.assertEqual(parsePriceInfo(soup_var).get("kaution"), "3000")

    def test_parseEnergy(self):
        # Mock HTML structure for energy box
        html = """
        <div data-testid="energy-pass-box">
            HWB 45 kwh/m²a Klasse B
            fGEE 0,85 Klasse A
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        data = parseEnergy(soup)
        
        self.assertEqual(data.get("hwb"), 45.0)
        self.assertEqual(data.get("fgee"), 0.85)
        
        # Check classes
        # 'B' in ENERGY_MAP is 6
        self.assertEqual(data.get("hwb_class"), 6)
        # 'A' in ENERGY_MAP is 7
        self.assertEqual(data.get("fgee_class"), 7)
        
        # Test missing box
        soup_none = BeautifulSoup("<div></div>", "html.parser")
        self.assertEqual(parseEnergy(soup_none), {})

    def test_parseAttributes(self):
        html = """
        <ul>
            <li data-testid="attribute-item">
                <span>Zimmer</span>
                <div>3</div>
            </li>
            <li data-testid="attribute-item">
                <span>Wohnfläche</span>
                <div>80 m²</div>
            </li>
        </ul>
        """
        soup = BeautifulSoup(html, "html.parser")
        attrs = parseAttributes(soup)
        self.assertEqual(attrs.get("Zimmer"), "3")
        self.assertEqual(attrs.get("Wohnfläche"), "80 m²")
        
        # Test empty
        self.assertEqual(parseAttributes(BeautifulSoup("", "html.parser")), {})

    @patch('scraper.source1_detail_scraper.fetch')
    def test_detailScraper(self, mock_fetch):
        # Mock successful fetch
        mock_fetch.return_value = """
        <html>
            <body>
                <div data-testid="energy-pass-box">HWB 50 Klasse C</div>
                <ul>
                    <li data-testid="attribute-item"><span>Key</span><div>Value</div></li>
                </ul>
                <div>Kaution: 1000</div>
            </body>
        </html>
        """
        
        result = detailScraper("http://fake.url")
        self.assertEqual(result.get("Key"), "Value")
        self.assertEqual(result.get("kaution"), "1000")
        self.assertEqual(result.get("hwb"), 50.0)
        # 'C' is 5
        self.assertEqual(result.get("hwb_class"), 5)

        # Mock fetch failure
        mock_fetch.return_value = None
        result_none = detailScraper("http://fail.url")
        self.assertEqual(result_none, {})

if __name__ == '__main__':
    unittest.main()
