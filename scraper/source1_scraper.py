"""
This module provides functionality to scrape real estate listings from source 1.
It extracts search result pages, parses the JSON data embedded in the HTML,
and optionally scrapes detailed information for each listing.
The data is then cleaned and stored in a database.
"""

import re, json, logging
import numpy as np
import pandas as pd
from datetime import date

from datamanipulation.loaders import loadBaseLinks
from database.db import get_connection
from database.db_insertion import upsertListings, insertHistory, updateListings
from scraper.source1_detail_scraper import detailScraper, fetch
from userinteraction.gui.guiData import getTerminateFlag

STATES = ("kaernten",)
UPPER_PAGE_RANGE = 3
ID_LENGTH = 4
ROWS = 100
BATCH_SIZE = 20
PAGE_SIZE = 20

OPTIONAL_DATA = [
    "has_carport",
    "has_elevator",
    "has_kitchen",
    "has_garage",
    "has_cellar",
    "has_parking",
    "has_closet",
    "has_balcony",
    "has_garden",
    "has_terrace",
    "has_loggia",
    "has_wintergarden",
    "balcony_size",
    "garden_size",
    "terrace_size",
    "loggia_size",
    "wintergarden_size",
    "hwb",
    "hwb_class",
    "fgee",
    "fgee_class"
]

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fillOptionalData(result):
    """
    Ensures that all keys defined in OPTIONAL_DATA are present in the result dictionary.
    If a value is missing or NaN, it is defaulted to 0.

    Args:
        result (dict): The dictionary containing listing data.
    Returns:
        dict: The updated dictionary with filled optional fields.
    """
    for key in OPTIONAL_DATA:
        val = result.get(key)

        if val is None or (isinstance(val, float) and np.isnan(val)):
            result[key] = 0

    return result

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



def buildPageUrls(base_links, pages=UPPER_PAGE_RANGE, rows=ROWS):
    """
    Constructs a list of URLs to scrape based on base links, states, and page ranges.

    Args:
        base_links (list): List of dicts containing base 'url' and 'fin_type'.
        pages (int): Number of pages to scrape per category.
        rows (int): Number of results per page.
    Returns:
        list: A list of dictionaries containing the constructed 'url' and 'fin_type'.
    """
    urls = []
    for l in base_links:
        for s in STATES:
            url = l["url"]

            url = url + s + "?rows=" + str(rows)

            for page in range(1, pages + 1):
                page_url = f"{url}&page={page}"
                urls.append({
                    "url": page_url,
                    "fin_type": l["fin_type"],
                })
    return urls

def extractId(url):
    """
    Extracts the numerical ID from the end of a listing URL.

    Args:
        url (str): The URL of the listing.

    Returns:
        int|None: The extracted ID as an integer, or None if no match is found.
    """
    match = re.search(r'-(\d+)/?$', url)
    return match.group(1) if match else None

def parseNextData(data, fin_type, scrape_details, total_items, processed_items, known_ids: set):
    """
    Parses the JSON data extracted from the __NEXT_DATA__ script tag.

    Args:
        data (dict): The parsed JSON data from the page.
        fin_type (str): The finance type (e.g., 'rent' or 'buy').
        scrape_details (bool): Whether to fetch additional details from the listing's own page.
        total_items (int): Total expected items for progress tracking.
        processed_items (int): Current count of processed items.
        known_ids (set(df["id"].values)): A set of already scraped ids.
    Returns:
        tuple: (list of parsed results, updated processed_items count).
        known_ids: a set of known ids
    """
    results = []
    known_results = []
    seen = set()

    try:
        asl = data["props"]["pageProps"]["searchResult"]["advertSummaryList"]

        if isinstance(asl, dict):
            items = asl.get("advertSummary", [])
        elif isinstance(asl, list):
            items = asl
        else:
            return [], processed_items

    except KeyError:
        return [], processed_items

    for item in items:
        processed_items += 1

        detail_link = getLink(item)
        detail_id = extractId(detail_link)
        progressBar(processed_items, total_items, detail_link or "no-link")

        if detail_id in known_ids:
            seen.add(detail_id)
            known_results.append({
                "id" : detail_id,
                "price" : getPrice(item),
                "rent" : getPrice(item),
                "scraped_at" : date.today(),
            })
            continue

        try:
            detail_data = detailScraper(detail_link) if (detail_link and scrape_details) else None

            if detail_data:
                detail_data = {k.lower(): v for k, v in detail_data.items()}

            id_ = str(item.get("id"))
            if not id_ or id_ in seen:
                continue
            seen.add(id_)

            lat, lon = getCoordinates(item)

            result = {
                "id": id_,
                "link": detail_link,
                "price": getPrice(item),
                "rent": getRent(item),
                "safety_deposit": getSafetyDeposit(detail_data),
                "living_area": getLivingArea(item),
                "estate_size": getEstateSize(item),
                "rooms": getRooms(item),
                "postcode": getPostcode(item),
                "lat": lat,
                "lon": lon,
                "location_quality": getLocationQuality(item),
                "property_type": getPropertyType(item),
                "finance_type": fin_type,
                "published": getPublished(item),
                "scraped_at": date.today(),
            }

            if detail_link:
                result.update(getHeating(detail_data) or {})
                result.update(getAccommodations(detail_data) or {})

            result = fillOptionalData(result)

            results.append(result)

        except Exception as e:
            print("Parse error: ", e)
            continue

    return results, processed_items, known_results


def extractNewData(html):
    """
    Extracts the JSON content from the __NEXT_DATA__ script tag in the HTML source.

    Args:
        html (str): The raw HTML content of the page.
    Returns:
        dict|None: The parsed JSON data or None if not found.
    """
    match = re.search(r'<script id="__NEXT_DATA__".*?>(.*?)</script>', html, re.DOTALL)
    if not match:
        return None

    return json.loads(match.group(1))


def getAttr(item, name):
    """
    Helper to extract a specific attribute value from the source 1 item attribute list.

    Args:
        item (dict): The listing item dictionary.
        name (str): The name of the attribute to retrieve.
    Returns:
        str|None: The attribute value or None.
    """
    for attr in item.get("attributes", {}).get("attribute", []):
        if attr.get("name") == name:
            values = attr.get("values", [])
            if values:
                return values[0]
    return None


def getLink(item):
    seo = getAttr(item, "SEO_URL")
    if not seo:
        return None
    return readSource() + "/iad/" + seo


# noinspection PyBroadException
def getPrice(item):
    price = getAttr(item, "PRICE")
    try:
        price = float(price)
    except:
        price = None
    return price


def getRent(item):
    rent = getAttr(item, "RENT/PER_MONTH_LETTINGS")
    return float(rent) if rent else None


def getSafetyDeposit(item):
    if not item:
        return None

    val = item.get("kaution")

    if not val or not isinstance(val, str):
        return None

    if "siehe preis" in val.lower():
        return None

    return getFeatureNumber(val)


def getLivingArea(item):
    val = getAttr(item, "ESTATE_SIZE/LIVING_AREA")
    return float(val) if val else None


def getEstateSize(item):
    val = getAttr(item, "ESTATE_SIZE")
    return float(val) if val else None


# noinspection PyBroadException
def getRooms(item):
    val = getAttr(item, "NUMBER_OF_ROOMS")
    try:
        num = int(val) if val else None
        return num if num != 0 else None
    except:
        return None


def getPostcode(item):
    return getAttr(item, "POSTCODE")


# noinspection PyBroadException
def getCoordinates(item):
    coords = getAttr(item, "COORDINATES")
    if not coords:
        return None, None
    try:
        lat, lon = coords.split(",")
        return float(lat), float(lon)
    except:
        return None, None


def getLocationQuality(item):
    val = getAttr(item, "LOCATION_QUALITY")
    return float(val) if val else None


def getPropertyType(item):
    return getAttr(item, "PROPERTY_TYPE")


def getPublished(item):
    val = getAttr(item, "PUBLISHED")
    return int(val) if val else None


def getHeating(item):
    h = item.get("heizung", "").lower() if item else ""
    return {
        "oil": int("öl" in h),
        "bio": int("bio" in h),
        "electro": int("elektrisch" in h),
        "pellets": int("pellets" in h),
        "photovoltaik": int("photovoltaik" in h),
        "geothermal": int("erdwärme" in h),
        "air_heating": int("luftwärmepumpe" in h),
        "floor_heating": int("fußbodenheizung" in h),
        "central_heating": int("hauszentralheizung" in h),
        "ceiling_heating": int("deckenheizung" in h),
        "oven_heating": int("holzofen" in h),
        "infrared_heating": int("infrarotheizung" in h)
    }


def hasFeature(item, key):
    if not item:
        return 0
    if key in item:
        return 1

    text = " ".join(str(v).lower() for v in item.values())
    return int(key in text)


def getFeatureNumber(val):
    if not val:
        return None

    if isinstance(val, (int, float)):
        return float(val)

    val = str(val)

    val = val.replace("€", "").replace(".", "").replace(",", ".")
    match = re.search(r"\d+\.?\d*", str(val))

    return float(match.group()) if match else None


def getAccommodations(item):
    if not item:
        return {}

    return {
        "has_carport": hasFeature(item, "carport"),
        "has_elevator": hasFeature(item, "fahrstuhl"),
        "has_kitchen": hasFeature(item, "küche"),
        "has_garage": hasFeature(item, "garage"),
        "has_cellar": hasFeature(item, "keller"),
        "has_parking": hasFeature(item, "parkplatz"),
        "has_closet": hasFeature(item, "abstellraum"),
        "has_balcony": hasFeature(item, "balkon"),
        "has_garden": hasFeature(item, "garten"),
        "has_terrace": hasFeature(item, "terrasse"),
        "has_loggia": hasFeature(item, "loggia"),
        "has_wintergarden": hasFeature(item, "wintergarten"),

        "balcony_size": getFeatureNumber(item.get("balkon")),
        "terrace_size": getFeatureNumber(item.get("terrasse")),
        "garden_size": getFeatureNumber(item.get("garten")),
        "loggia_size": getFeatureNumber(item.get("loggia")),
        "wintergarden_size": getFeatureNumber(item.get("wintergarten")),

        "hwb": getFeatureNumber(item.get("hwb")),
        "hwb_class": item.get("hwb energieklasse") if item else None,
        "fgee": getFeatureNumber(item.get("fgee")),
        "fgee_class": item.get("fgee energieklasse") if item else None,
    }


def cleanDuplicates(buffer, seen_ids):
    """
    Removes duplicates and invalid entries (missing price or area) from the current batch.

    Args:
        buffer (list): List of scraped listing dictionaries.
        seen_ids (set): Set of IDs already processed in this session.
    Returns:
        list: Filtered list of listings.
    """
    new_buffer = []
    for l in buffer:
        if l["id"] in seen_ids:
            continue
        elif l["price"] is None:
            continue
        elif l["living_area"] is None:
            continue
        else:
            seen_ids.add(l["id"])
            new_buffer.append(l)
    return new_buffer


def progressBar(current, total, url, length=30):
    """
    Prints a simple progress bar to the console.

    Args:
        current (int): Current progress.
        total (int): Total target.
        url (str): Current URL being processed.
        length (int): Character length of the bar.
    """
    filled = int(length * current // total)
    bar = "=" * (filled - 1) + ">" if filled > 0 else ">"
    bar = bar.ljust(length)

    print(f"\r[{bar}] {current}/{total} | {url}", end="", flush=True)

def getAllIds(conn):
    """
    Retrieves all existing listing IDs from the database to know which listings has been seen already
    and which we only need to update.

    Args:
        conn: Database connection object.
    """
    return pd.read_sql("SELECT id, price, scraped_at FROM listings", conn)


def baseScraper(pages, scrape_details=True, rows=ROWS):
    """
    Main entry point for the scraping process. Orchestrates URL building,
    fetching, parsing, and database insertion.

    Args:
        pages (int): Number of pages to scrape.
        scrape_details (bool): Whether to perform deep scraping of individual listings.
        rows (int): Results per page.
    """
    base_links = loadBaseLinks()
    buffer = []
    history_buffer = []
    seen_ids = set()
    known_listings = 0
    new_listings = 0

    counter_known_listings = 0
    counter_new_listings = 0

    conn = get_connection()
    cur = conn.cursor()
    df_known_ids = getAllIds(conn)

    if not conn or not cur:
        logging.error("Connection and / or cursor to db failed")
        return

    urls = buildPageUrls(base_links, pages=pages, rows=rows)
    total_items = len(urls) * rows
    processed_items = 0

    print(f"Scraping {len(urls)} pages...\n")

    for i, u in enumerate(urls, start=1):
        html = fetch(u["url"])
        if not html:
            continue

        if "<title>" in html:
            title = html.split("<title>")[1].split("</title>")[0]
            logging.error("Blocked by Bot-stop INFO: %s", title)

        data = extractNewData(html)
        if not data:
            logging.info("No NEXT_DATA found in %s page %d. Skipping...", u["url"], i)
            continue

        page_data, processed_items, known_page_data = parseNextData(
            data,
            u["fin_type"],
            scrape_details=scrape_details,
            total_items=total_items,
            processed_items=processed_items,
            known_ids=set(df_known_ids["id"].values)
        )
        known_listings += len(known_page_data)
        new_listings += len(page_data)

        counter_new_listings += len(page_data)
        counter_known_listings += len(known_page_data)

        page_data = [
            d for d in page_data
            if d.get("lat") is not None and d.get("lon") is not None
        ]
        cleaned_page_data = cleanDuplicates(page_data, seen_ids)
        buffer.extend(cleaned_page_data)
        history_buffer.extend(known_page_data)

        if getTerminateFlag():
            cur.close()
            conn.close()
            return

        try:
            if len(buffer) >= BATCH_SIZE or i == len(urls) or len(history_buffer) >= BATCH_SIZE:
                upsertListings(buffer, conn=conn, cur=cur, PAGE_SIZE=PAGE_SIZE)
                insertHistory(history_buffer, cur=cur, PAGE_SIZE=PAGE_SIZE)
                updateListings(history_buffer, cur=cur, PAGE_SIZE=PAGE_SIZE)

                if counter_new_listings > 100 or counter_known_listings > 100:
                    logging.info(f"Transfered {counter_new_listings} new listings and {counter_known_listings} known listings")
                    counter_new_listings = 0
                    counter_known_listings = 0

                conn.commit()

                history_buffer.clear()
                buffer.clear()

        except Exception:
            conn.rollback()
            logging.exception("Failed to insert batch into Database")

    logging.info(f"Found {known_listings} known listings and {new_listings} new listings")

    cur.close()
    conn.close()


if __name__ == "__main__":
    baseScraper(pages=3)
