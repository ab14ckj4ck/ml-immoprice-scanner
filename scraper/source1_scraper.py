"""
This module provides functionality to scrape real estate listings from source 1.
It extracts search result pages, parses the JSON data embedded in the HTML,
and optionally scrapes detailed information for each listing.
The data is then cleaned and stored in a database.
"""

from datetime import date
from datamanipulation.loaders import loadBaseLinks
from database.db import getConnection
from database.db_insertion import upsertListings, insertHistory, updateListings
from scraper.source1_detail_scraper import detailScraper, fetch
from userinteraction.gui.guiData import getTerminateFlag
from utils.enums import Listings, Mappings, ScraperValues

import re, json, logging
import numpy as np
import pandas as pd
import time


logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
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
    for key in Mappings.OPTIONAL_DATA:
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


def buildPageUrls(base_links, pages=5, rows=30):
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
        for s in ScraperValues.STATES:
            url = l[Listings.URL]

            url = url + s + "?rows=" + str(rows)

            for page in range(1, pages + 1):
                page_url = f"{url}&page={page}"
                urls.append({
                    Listings.URL: page_url,
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
        known_ids (set(df[Listings.ID].values)): A set of already scraped ids.
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
                Listings.ID: detail_id,
                Listings.PRICE: getPrice(item),
                Listings.RENT: getPrice(item),
                Listings.SCRAPED_AT: date.today(),
            })
            continue

        try:
            detail_data = detailScraper(detail_link) if (detail_link and scrape_details) else None
            if not detail_data:
                continue

            if detail_data:
                detail_data = {k.lower(): v for k, v in detail_data.items()}

            id_ = str(item.get(Listings.ID))
            if not id_ or id_ in seen:
                continue
            seen.add(id_)

            lat, lon = getCoordinates(item)

            result = {
                Listings.ID: id_,
                Listings.URL: detail_link,
                Listings.PRICE: getPrice(item),
                Listings.RENT: getRent(item),
                Listings.SAFETY_DEPOSIT: getSafetyDeposit(detail_data),
                Listings.LIVING_AREA: getLivingArea(item),
                Listings.ESTATE_SIZE: getEstateSize(item),
                Listings.ROOMS: getRooms(item),
                Listings.POSTCODE: getPostcode(item),
                Listings.STATE: data["query"]["seopath"][1],
                Listings.LAT: lat,
                Listings.LON: lon,
                Listings.LOCATION_QUALITY: getLocationQuality(item),
                Listings.PROPERTY_TYPE: getPropertyType(item),
                Listings.FINANCE_TYPE: fin_type,
                Listings.PUBLISHED: getPublished(item),
                Listings.SCRAPED_AT: date.today(),
            }

            if detail_link:
                result.update(getHeating(detail_data) or {})
                result.update(getAccommodations(detail_data) or {})

            result = fillOptionalData(result)

            results.append(result)

        except Exception as e:
            logging.exception(f"Exception while parsing: {detail_link}: ")
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
    """
    Constructs the full URL for a listing using its SEO_URL attribute.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        str|None: The full URL or None if SEO_URL is missing.
    """
    seo = getAttr(item, "SEO_URL")
    if not seo:
        return None
    return readSource() + "/iad/" + seo


# noinspection PyBroadException
def getPrice(item):
    """
    Extracts the PRICE attribute and converts it to a float.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        float|None: The price as a float, or None if extraction fails.
    """
    price = getAttr(item, "PRICE")
    try:
        price = float(price)
    except:
        price = None
    return price


def getRent(item):
    """
    Extracts the monthly rent attribute and converts it to a float.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        float|None: The rent as a float, or None if missing.
    """
    rent = getAttr(item, "RENT/PER_MONTH_LETTINGS")
    return float(rent) if rent else None


def getSafetyDeposit(item):
    """
    Extracts the safety deposit (Kaution) from the detail data.

    Args:
        item (dict): The detail data dictionary.
    Returns:
        float|None: The deposit amount as a float, or None if not applicable.
    """
    if not item:
        return None

    val = item.get("kaution")

    if not val or not isinstance(val, str):
        return None

    if "siehe preis" in val.lower():
        return None

    return getFeatureNumber(val)


def getLivingArea(item):
    """
    Extracts the living area size from the item attributes.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        float|None: The living area in square meters.
    """
    val = getAttr(item, "ESTATE_SIZE/LIVING_AREA")
    return float(val) if val else None


def getEstateSize(item):
    """
    Extracts the total estate/plot size from the item attributes.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        float|None: The estate size in square meters.
    """
    val = getAttr(item, "ESTATE_SIZE")
    return float(val) if val else None


# noinspection PyBroadException
def getRooms(item):
    """
    Extracts the number of rooms from the item attributes.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        int|None: The number of rooms, or None if 0 or invalid.
    """
    val = getAttr(item, "NUMBER_OF_ROOMS")
    try:
        num = int(val) if val else None
        return num if num != 0 else None
    except:
        return None


def getPostcode(item):
    """
    Extracts the postcode from the item attributes.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        str|None: The postcode.
    """
    return getAttr(item, "POSTCODE")


# noinspection PyBroadException
def getCoordinates(item):
    """
    Extracts and splits the COORDINATES attribute into latitude and longitude.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        tuple: (latitude float|None, longitude float|None).
    """
    coords = getAttr(item, "COORDINATES")
    if not coords:
        return None, None
    try:
        lat, lon = coords.split(",")
        return float(lat), float(lon)
    except:
        return None, None


def getLocationQuality(item):
    """
    Extracts the location quality score.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        float|None: The location quality value.
    """
    val = getAttr(item, "LOCATION_QUALITY")
    return float(val) if val else None


def getPropertyType(item):
    """
    Extracts the property type (e.g., House, Apartment).

    Args:
        item (dict): The listing item dictionary.
    Returns:
        str|None: The property type.
    """
    return getAttr(item, "PROPERTY_TYPE")


def getPublished(item):
    """
    Extracts the publication timestamp.

    Args:
        item (dict): The listing item dictionary.
    Returns:
        int|None: The publication date as an integer.
    """
    val = getAttr(item, "PUBLISHED")
    return int(val) if val else None


def getHeating(item):
    """
    Parses heating information from the detail data and returns a mapping of heating types.

    Args:
        item (dict): The detail data dictionary.
    Returns:
        dict: A dictionary of boolean flags (0 or 1) for various heating types.
    """
    h = item.get("heizung", "").lower() if item else ""
    return {
        Listings.IS_OIL: int("öl" in h),
        Listings.IS_BIO: int("bio" in h),
        Listings.IS_ELECTRO: int("elektrisch" in h),
        Listings.IS_PELLETS: int("pellets" in h),
        Listings.IS_PHOTOVOLTAIK: int("photovoltaik" in h),
        Listings.IS_GEOTHERMAL: int("erdwärme" in h),
        Listings.IS_AIR_HEATING: int("luftwärmepumpe" in h),
        Listings.IS_FLOOR: int("fußbodenheizung" in h),
        Listings.IS_CENTRAL: int("hauszentralheizung" in h),
        Listings.IS_CEILING: int("deckenheizung" in h),
        Listings.IS_OVEN: int("holzofen" in h),
        Listings.IS_INFRARED: int("infrarotheizung" in h)
    }


def hasFeature(item, key):
    """
    Checks if a specific feature keyword exists in the detail data keys or values.

    Args:
        item (dict): The detail data dictionary.
        key (str): The keyword to search for.
    Returns:
        int: 1 if found, 0 otherwise.
    """
    if not item:
        return 0
    if key in item:
        return 1

    text = " ".join(str(v).lower() for v in item.values())
    return int(key in text)


def getFeatureNumber(val):
    """
    Cleans a string value (removing currency symbols and formatting) and extracts the first number.

    Args:
        val (str|int|float): The value to parse.
    Returns:
        float|None: The extracted number as a float.
    """
    if not val:
        return None

    if isinstance(val, (int, float)):
        return float(val)

    val = str(val)

    val = val.replace("€", "").replace(".", "").replace(",", ".")
    match = re.search(r"\d+\.?\d*", str(val))

    return float(match.group()) if match else None


def getAccommodations(item):
    """
    Parses accommodation features (balcony, garage, etc.) and energy ratings from detail data.

    Args:
        item (dict): The detail data dictionary.
    Returns:
        dict: A dictionary containing feature flags and sizes.
    """
    if not item:
        return {}

    return {
        Listings.HAS_CARPORT: hasFeature(item, "carport"),
        Listings.HAS_ELEVATOR: hasFeature(item, "fahrstuhl"),
        Listings.HAS_KITCHEN: hasFeature(item, "küche"),
        Listings.HAS_GARAGE: hasFeature(item, "garage"),
        Listings.HAS_CELLAR: hasFeature(item, "keller"),
        Listings.HAS_PARKING: hasFeature(item, "parkplatz"),
        Listings.HAS_CLOSET: hasFeature(item, "abstellraum"),
        Listings.HAS_BALCONY: hasFeature(item, "balkon"),
        Listings.HAS_GARDEN: hasFeature(item, "garten"),
        Listings.HAS_TERRACE: hasFeature(item, "terrasse"),
        Listings.HAS_LOGGIA: hasFeature(item, "loggia"),
        Listings.HAS_WINTERGARDEN: hasFeature(item, "wintergarten"),

        Listings.BALCONY_SIZE: getFeatureNumber(item.get("balkon")),
        Listings.TERRACE_SIZE: getFeatureNumber(item.get("terrasse")),
        Listings.GARDEN_SIZE: getFeatureNumber(item.get("garten")),
        Listings.LOGGIA_SIZE: getFeatureNumber(item.get("loggia")),
        Listings.WINTERGARDEN_SIZE: getFeatureNumber(item.get("wintergarten")),

        Listings.HWB: getFeatureNumber(item.get("hwb")),
        Listings.HWB_CLASS: item.get("hwb energieklasse") if item else None,
        Listings.FGEE: getFeatureNumber(item.get("fgee")),
        Listings.FGEE_CLASS: item.get("fgee energieklasse") if item else None,
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
        if l[Listings.ID] in seen_ids:
            continue
        elif l[Listings.PRICE] is None:
            continue
        elif l[Listings.LIVING_AREA] is None:
            continue
        else:
            seen_ids.add(l[Listings.ID])
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


def baseScraper(pages, scrape_details=True, rows=30):
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
    sleep_time = 1
    status_code = 0

    conn = getConnection()
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
        html = ""

        while status_code != 200:
            html, status_code = fetch(u[Listings.URL])
            if not html:
                sleep(5)
                continue

            if status_code != 200:
                sleep_time = min(sleep_time * 2, ScraperValues.MAX_SLEEP_TIME)
            else:
                sleep_time = max(sleep_time * 0.9, ScraperValues.MIN_SLEEP_TIME)

            time.sleep(sleep_time)

        status_code = 0
        if html != "" and "<title>" in html:
            title = html.split("<title>")[1].split("</title>")[0]
            logging.error("Blocked by Bot-stop INFO: %s", title)

        data = extractNewData(html)
        if not data:
            logging.info("No NEXT_DATA found in %s page %d. Skipping...", u[Listings.URL], i)
            continue

        page_data, processed_items, known_page_data = parseNextData(
            data,
            u["fin_type"],
            scrape_details=scrape_details,
            total_items=total_items,
            processed_items=processed_items,
            known_ids=set(df_known_ids[Listings.ID].values)
        )
        known_listings += len(known_page_data)
        new_listings += len(page_data)

        counter_new_listings += len(page_data)
        counter_known_listings += len(known_page_data)

        page_data = [
            d for d in page_data
            if d.get(Listings.LAT) is not None and d.get(Listings.LON) is not None
        ]
        cleaned_page_data = cleanDuplicates(page_data, seen_ids)
        buffer.extend(cleaned_page_data)
        history_buffer.extend(known_page_data)

        if getTerminateFlag():
            cur.close()
            conn.close()
            return

        try:
            if len(buffer) >= ScraperValues.BATCH_SIZE or i == len(urls) or len(history_buffer) >= ScraperValues.BATCH_SIZE:
                upsertListings(buffer, conn=conn, cur=cur, PAGE_SIZE=ScraperValues.PAGE_SIZE)
                insertHistory(history_buffer, cur=cur, PAGE_SIZE=ScraperValues.PAGE_SIZE)
                updateListings(history_buffer, cur=cur, PAGE_SIZE=ScraperValues.PAGE_SIZE)

                if counter_new_listings > 100 or counter_known_listings > 100:
                    logging.info(
                        f"Transferred {counter_new_listings} new listings and {counter_known_listings} known listings")
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
