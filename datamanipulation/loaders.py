import xml.etree.ElementTree as ET

VALID_IMMO_TYPES = ("house", "apartment", "projects")
VALID_FIN_TYPES = ("rent", "buy")  # TODO implement "project" handling

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

    for link_group in root.findall("link"):
        if link_group.get("category") != name:
            continue

        for immo in link_group.findall("immo"):
            immo_type = immo.get("category")
            if immo_type not in VALID_IMMO_TYPES:
                continue

            for t in immo.findall("type"):
                fin_type = t.get("category")
                if fin_type not in VALID_FIN_TYPES:
                    continue

                link = t.find("link").text

                links.append({
                    "url": link,
                    "fin_type": fin_type,
                })

    return links

def loadLocationData(path, target):
    """
    Loads geographic coordinates for specific locations from an XML file.

    :param path: Path to the XML file.
    :param target: The type of location to extract ('cities' or 'lakes').
    :return: A list of dictionaries with name, latitude, and longitude.
    """
    tree = ET.parse(path)
    root = tree.getroot()

    dataset = []

    if target == "cities":
        elements = root.findall("city")
    elif target == "lakes":
        elements = root.findall("lake")
    else:
        elements = []

    for d in elements:
        data = {
            "name": d.get("name"),
            "lat": float(d.find("lat").text),
            "lon": float(d.find("lon").text),
        }
        dataset.append(data)

    return dataset