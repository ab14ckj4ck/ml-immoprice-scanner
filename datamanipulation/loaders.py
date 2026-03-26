from utils.enums import LoaderValues

import xml.etree.ElementTree as ET
import logging



logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def readSource(path="data/source1-name.txt"):
    """
    Reads the content of a file from the specified path and returns it as a string.

    Args:
        path (str): The file path to read from.
    Returns:
        str: The content of the file.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except ValueError:
        logging.exception("Source file not found.")

def loadBaseLinks(path="data/base-links.xml"):
    """
    Parses an XML file containing base URLs for real estate listings.

    :param path: Path to the XML file.
    :return: A list of dictionaries containing the URL and financial type (rent/buy).
    """
    tree = ET.parse(path)
    root = tree.getroot()

    links = []
    name = readSource()

    for link_group in root.findall(LoaderValues.LINK):
        if link_group.get(LoaderValues.CATEGORY) != name:
            continue

        for immo in link_group.findall(LoaderValues.IMMO):
            immo_type = immo.get(LoaderValues.CATEGORY)
            if immo_type not in LoaderValues.VALID_IMMO_TYPES:
                continue

            for t in immo.findall(LoaderValues.TYPE):
                fin_type = t.get(LoaderValues.CATEGORY)
                if fin_type not in LoaderValues.VALID_FIN_TYPES:
                    continue

                link = t.find(LoaderValues.LINK).text

                links.append({
                    LoaderValues.URL: link,
                    LoaderValues.FIN_TYPE: fin_type,
                })

    return links

def loadLocationData(path, target):
    """
    Loads geographic coordinates for specific locations from an XML file.

    :param path: Path to the XML file.
    :param target: The type of location to extract.
    :return: A list of dictionaries with name, latitude, and longitude.
    """
    tree = ET.parse(path)
    root = tree.getroot()

    elements = root.findall(target)
    dataset = []

    for d in elements:
        data = {
            LoaderValues.NAME: d.get(LoaderValues.NAME),
            LoaderValues.LAT: float(d.find(LoaderValues.LAT).text),
            LoaderValues.LON: float(d.find(LoaderValues.LON).text),
        }
        dataset.append(data)

    return dataset