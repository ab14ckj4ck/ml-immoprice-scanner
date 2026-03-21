import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET
from datamanipulation.loaders import loadBaseLinks, loadLocationData

def readSource(path="data/source1-name.txt"):
    """
    Reads the content of a file from the specified path and returns it as a string.

    Args:
        path (str): The file path to read from.
    Returns:
        str: The content of the file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


class TestLoaders(unittest.TestCase):

    @patch('xml.etree.ElementTree.parse')
    def test_loadBaseLinks(self, mock_parse):
        xml_content = f"""
        <root>
            <link category="{readSource()}">
                <immo category="house">
                    <type category="buy">
                        <link>http://example.com/house/buy</link>
                    </type>
                    <type category="rent">
                        <link>http://example.com/house/rent</link>
                    </type>
                    <type category="invalid">
                        <link>http://example.com/house/invalid</link>
                    </type>
                </immo>
                <immo category="invalid_immo">
                    <type category="buy">
                        <link>http://example.com/invalid/buy</link>
                    </type>
                </immo>
            </link>
            <link category="other">
                <immo category="house">
                    <type category="buy">
                        <link>http://example.com/other</link>
                    </type>
                </immo>
            </link>
        </root>
        """
        # Mocking ET.parse().getroot() to return the parsed XML from string
        root = ET.fromstring(xml_content)
        mock_tree = MagicMock()
        mock_tree.getroot.return_value = root
        mock_parse.return_value = mock_tree

        links = loadBaseLinks("dummy_path")

        self.assertEqual(len(links), 2)
        expected_urls = [
            "http://example.com/house/buy",
            "http://example.com/house/rent"
        ]
        extracted_urls = [l["url"] for l in links]
        self.assertListEqual(extracted_urls, expected_urls)
        
        self.assertEqual(links[0]["fin_type"], "buy")

    @patch('xml.etree.ElementTree.parse')
    def test_loadLocationData(self, mock_parse):
        xml_content = """
        <root>
            <city name="Vienna">
                <lat>48.2082</lat>
                <lon>16.3738</lon>
            </city>
            <lake name="Wörthersee">
                <lat>46.6267</lat>
                <lon>14.1368</lon>
            </lake>
        </root>
        """
        root = ET.fromstring(xml_content)
        mock_tree = MagicMock()
        mock_tree.getroot.return_value = root
        mock_parse.return_value = mock_tree

        # Test cities
        cities = loadLocationData("dummy_path", "cities")
        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0]["name"], "Vienna")
        self.assertEqual(cities[0]["lat"], 48.2082)

        # Test lakes
        lakes = loadLocationData("dummy_path", "lakes")
        self.assertEqual(len(lakes), 1)
        self.assertEqual(lakes[0]["name"], "Wörthersee")

        # Test invalid target
        none = loadLocationData("dummy_path", "invalid")
        self.assertEqual(len(none), 0)

if __name__ == '__main__':
    unittest.main()
