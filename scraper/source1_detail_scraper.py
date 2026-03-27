"""
This module provides functionality to scrape detailed real estate information from source 1.

It includes functions to fetch HTML content with basic anti-bot measures, parse specific
attributes like price, deposit (Kaution), energy certificates (HWB, fGEE), and general
listing attributes from the page structure.
"""

from bs4 import BeautifulSoup
from utils.enums import ScraperValues

import requests, re, time, random, logging

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
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
    response = None

    for attempt in range(retries):
        if random.random() < 0.05:
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
            break

        except Exception as e:
            logging.exception("Fetch error: %s", e)

    return response.text, response.status_code


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
        data["hwb_class"] = ScraperValues.ENERGY_MAP.get(cls, 0)

    if fgee_class:
        cls = fgee_class.group(1).upper()
        data["fgee_class"] = ScraperValues.ENERGY_MAP.get(cls, 0)

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
        divs = item.find_all("div")
        
        if not title or not divs:
            continue

        value = divs[-1]
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
    sleep_time = 1
    status_code = 0
    html = ""
    while status_code != 200:
        html, status_code = fetch(url)
        if not html:
            logging.warning("Unreachable detail page in listings: %s", url)
            return {}

        if status_code != 200:
            sleep_time = min(sleep_time * 2, ScraperValues.MAX_SLEEP_TIME)
        else:
            sleep_time = max(sleep_time * 0.9, ScraperValues.MIN_SLEEP_TIME)

        time.sleep(sleep_time)

    status_code = 0

    soup = BeautifulSoup(html, "lxml")

    t = {}

    attributes = parseAttributes(soup)
    price_data = parsePriceInfo(soup)
    energy_data = parseEnergy(soup)


    t.update(attributes)
    t.update(price_data)
    t.update(energy_data)

    return t
