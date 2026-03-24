"""
This module provides functionality to scrape detailed real estate information from source 1.

It includes functions to fetch HTML content with basic anti-bot measures, parse specific
attributes like price, deposit (Kaution), energy certificates (HWB, fGEE), and general
listing attributes from the page structure.
"""

import requests, re, time, random, logging
from bs4 import BeautifulSoup

ENERGY_MAP = {
    "A++": 9,
    "A+": 8,
    "A": 7,
    "B": 6,
    "C": 5,
    "D": 4,
    "E": 3,
    "F": 2,
    "G": 1
}


logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def readSource(path="data/source1.txt"):
    """
    Reads the content of a file from the specified path and returns it as a string.

    Args:
        path (str): The file path to read from.
    Returns:
        str: The content of the file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

session = requests.Session()
session.get(readSource())

def fetch(url, retries=3):
    """
    Fetches the HTML content of a given URL using a shared session.

    Args:
        url (str): The URL to fetch.
        retries (int): Number of attempts in case of failure or rate limiting.

    Returns:
        str: The HTML content if successful, None otherwise.
    """
    for attempt in range(retries):
        time.sleep(random.uniform(2, 6))

        if random.random() < 0.1:
            time.sleep(random.uniform(5,random.uniform(5,15)))

        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Mozilla/5.0 (X11; Linux x86_64)"
            ]),
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8",
            "Connection": "keep-alive"
        }

        try:
            response = session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.text

            if response.status_code == 429:
                print("⚠️ Rate limited → sleeping...")
                time.sleep(random.uniform(20, 60))

        except Exception as e:
            print("Fetch error:", e)

    return None


# noinspection PyArgumentList
def parsePriceInfo(soup):
    """
    Extracts pricing information not found in standard attribute lists, specifically 'Kaution'.

    Args:
        soup (BeautifulSoup): The parsed HTML of the page.

    Returns:
        dict: A dictionary containing the 'kaution' value if found.
    """
    data = {}

    text = soup.get_text(" ", strip=True)

    match = re.search(r"Kaution:\s*€?\s*([\d\.,]+)", text, re.IGNORECASE)
    if match:
        data["kaution"] = match.group(1)

    return data


# noinspection PyArgumentList
def parseEnergy(soup):
    """
    Parses energy certificate details (HWB and fGEE) and their respective classes.

    Args:
        soup (BeautifulSoup): The parsed HTML of the page.

    Returns:
        dict: Numeric values for HWB/fGEE and mapped integer values for energy classes.
    """
    data = {}

    box = soup.find("div", {"data-testid": "energy-pass-box"})
    if not box:
        return data

    text = box.get_text(" ", strip=True).lower()

    hwb = re.search(r"hwb.*?(\d+\.?\d*)", text)
    fgee = re.search(r"fgee.*?(\d+[,\.]?\d*)", text)

    hwb_class = re.search(r"hwb.*?klasse\s*([a-g]\+*)", text)
    fgee_class = re.search(r"fgee.*?klasse\s*([a-g]\+*)", text)

    if hwb:
        data["hwb"] = float(hwb.group(1))

    if fgee:
        val = fgee.group(1).replace(",", ".")
        data["fgee"] = float(val)

    if hwb_class:
        cls = hwb_class.group(1).upper()
        data["hwb_class"] = ENERGY_MAP.get(cls, 0)

    if fgee_class:
        cls = fgee_class.group(1).upper()
        data["fgee_class"] = ENERGY_MAP.get(cls, 0)

    return data

def parseAttributes(soup):
    """
    Parses the standard attribute list (e.g., 'Zimmer', 'Wohnfläche') from the listing.

    Args:
        soup (BeautifulSoup): The parsed HTML of the page.

    Returns:
        dict: Key-value pairs of the listing's attributes.
    """
    attributes = {}

    items = soup.find_all("li", {"data-testid": "attribute-item"})

    for item in items:
        title = item.find("span")
        value = item.find_all("div")[-1]

        if not title or not value:
            continue

        key = title.text.strip()
        val = value.text.strip()

        attributes[key] = val

    return attributes



def detailScraper(url):
    """
    Main entry point to scrape all available details from a source 1 listing URL.

    Args:
        url (str): The full URL of the detail page.

    Returns:
        dict: A combined dictionary of all scraped attributes, price info, and energy data.
    """
    html = fetch(url)
    if not html:
        logging.warning("Unreachable detail page in listings: %s", url)
        return {}

    soup = BeautifulSoup(html, "lxml")

    t = {}

    attributes = parseAttributes(soup)
    price_data = parsePriceInfo(soup)
    energy_data = parseEnergy(soup)


    t.update(attributes)
    t.update(price_data)
    t.update(energy_data)

    return t