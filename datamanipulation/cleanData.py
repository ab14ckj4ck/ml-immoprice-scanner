"""
This module provides functions for cleaning and preprocessing real estate data.

It includes functionality for:
- Loading data from a database and external XML location files.
- Calculating derived features like price per m2, ratios, and distances to landmarks.
- Filtering outliers and handling missing values.
- Inserting processed features back into the database.
"""
from database.db import get_connection
from database.db_insertion import insertFeatures
from datamanipulation.loaders import loadLocationData
import pandas as pd
import numpy as np
import sys, logging

CITIES_FILE = "data/cities.xml"
LAKES_FILE = "data/lakes.xml"
URBAN_THRESHOLD = 25
PAGES = 20
OPTIONAL_FEATURES = [
    "balcony_ratio",
    "garden_ratio",
    "loggia_ratio",
    "wintergarden_ratio",
    "terrace_ratio"
]

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def loadData(conn):
    """Loads all records from the listings table."""
    return pd.read_sql("SELECT * FROM listings", conn)


def quantileElimination(df, col, q_low_val=0.05, q_high_val=0.95):
    """Removes outliers from a dataframe based on quantile thresholds for a specific column."""
    df = df.copy()
    q_low = df[col].quantile(q_low_val)
    q_high = df[col].quantile(q_high_val)
    return df[(df[col] >= q_low) & (df[col] <= q_high)]


def minMax(df, col):
    """Applies Min-Max normalization to a column, creating a new 'norm_' prefixed column."""
    min_val = df[col].min()
    max_val = df[col].max()

    if max_val == min_val:
        df["norm_" + col] = 0
    else:
        df["norm_" + col] = (df[col] - min_val) / (max_val - min_val)

    return df


def getLogNorm(df, col):
    """Applies a natural logarithm transformation to a column."""
    df["log_" + col] = np.log(df[col].where(df[col] > 0))
    return df


def getRatio(df, col1, col2, new_col):
    """Calculates the ratio between two columns and handles division by zero."""
    df[new_col] = df[col1] / df[col2].replace(0, np.nan)
    return df


def getLocations():
    """Loads city and lake location data from XML files."""
    cities = loadLocationData(path=CITIES_FILE, target="cities")
    lakes = loadLocationData(path=LAKES_FILE, target="lakes")
    return cities, lakes


def haversine(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance between two points on Earth in kilometers."""
    R = 6371.0

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = np.sin(d_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def computeDistances(df, cities, lakes):
    """Computes distances from each listing to the nearest city, lake, and specific hubs."""
    df["distance_nearest_city"] = df.apply(
        lambda row: min(
            haversine(row["lat"], row["lon"], c["lat"], c["lon"])
            for c in cities
        ) if pd.notnull(row["lat"]) else np.nan,
        axis=1
    )

    df["distance_nearest_lake"] = df.apply(
        lambda row: min(
            haversine(row["lat"], row["lon"], l["lat"], l["lon"])
            for l in lakes
        ) if pd.notnull(row["lat"]) else np.nan,
        axis=1
    )

    def dist_to(row, lat, lon):
        if pd.isnull(row["lat"]):
            return np.nan
        return haversine(row["lat"], row["lon"], lat, lon)

    df["distance_villach"] = df.apply(lambda r: dist_to(r, 46.6103, 13.8558), axis=1)
    df["distance_klagenfurt"] = df.apply(lambda r: dist_to(r, 46.6247, 14.3053), axis=1)

    return df


def getIsUrban(df):
    """Flags listings as urban if they are within the defined URBAN_THRESHOLD distance of a city."""
    df["is_urban"] = (df["distance_nearest_city"] <= URBAN_THRESHOLD).astype(int)
    return df


def getUrbanPricePerM2(df):
    """Calculates price per m2 specifically for urban areas (0 for non-urban)."""
    df["urban_ppm2"] = df["ppm2"] * df["is_urban"]
    return df


def setHousingType(df):
    """Categorizes listings into based on property_type lists."""
    df["is_efh"] = (df["property_type"] == "Einfamilienhaus").astype(int)
    df["is_mfh"] = (df["property_type"] == "Mehrfamilienhaus").astype(int)
    df["is_lh"] = (df["property_type"] == "Landhaus").astype(int)
    df["is_villa"] = (df["property_type"] == "Villa").astype(int)
    df["is_dhh"] = (df["property_type"] == "Doppelhaushälfte").astype(int)
    df["is_sbc"] = (df["property_type"] == "Schloss/Burg/Chalet").astype(int)
    df["is_rh"] = (df["property_type"] == "Reihenhaus").astype(int)
    df["is_ab"] = (df["property_type"] == "Almhütte/Berghütte").astype(int)
    df["is_bh"] = (df["property_type"] == "Bauernhaus").astype(int)
    df["is_gh"] = (df["property_type"] == "Genossenschaftshaus").astype(int)

    df["is_dgw"] = (df["property_type"] == "Dachgeschoßwohnung").astype(int)
    df["is_egw"] = (df["property_type"] == "Erdgeschoßwohnung").astype(int)
    df["is_gc"] = (df["property_type"] == "Garconniere").astype(int)
    df["is_gw"] = (df["property_type"] == "Genossenschaftswohnung").astype(int)
    df["is_ms"] = (df["property_type"] == "Maisonette").astype(int)
    df["is_phw"] = (df["property_type"] == "Penthauswohnung").astype(int)
    df["is_apt"] = (df["property_type"] == "Wohnung").astype(int)
    df["is_wg"] = (df["property_type"] == "WG").astype(int)
    return df


def getAge(df):
    df = df.copy()

    df["published"] = pd.to_datetime(
        df["published"],
        unit="ms",
        errors="coerce"
    )

    df["scraped_at"] = pd.to_datetime(
        df["scraped_at"],
        errors="coerce"
    )

    df["days_since_publish"] = (
            df["scraped_at"] - df["published"]
    ).dt.days

    df["days_since_publish"] = df["days_since_publish"].clip(lower=0)

    return df


def cleanUp(df):
    """Orchestrates the feature engineering process for a dataframe."""
    df = minMax(df, "price")
    df = getLogNorm(df, "price")

    df = getRatio(df, "price", "living_area", "ppm2")
    df["log_ppm2"] = np.log(df["ppm2"].where(df["ppm2"] > 0))
    df = getRatio(df, "estate_size", "living_area", "estate_ratio")
    df = getRatio(df, "rooms", "living_area", "rpm2")
    df = getRatio(df, "price", "rooms", "ppr")

    df = getRatio(df, "balcony_size", "living_area", "balcony_ratio")
    df = getRatio(df, "garden_size", "living_area", "garden_ratio")
    df = getRatio(df, "terrace_size", "living_area", "terrace_ratio")
    df = getRatio(df, "loggia_size", "living_area", "loggia_ratio")
    df = getRatio(df, "wintergarden_size", "living_area", "wintergarden_ratio")

    df = getRatio(df, "rooms", "estate_size", "rooms_per_property")

    cities, lakes = getLocations()

    df = computeDistances(df, cities, lakes)

    df = getIsUrban(df)
    df = getUrbanPricePerM2(df)

    df = setHousingType(df)
    df = getAge(df)
    df = getRatio(df, "living_area", "rooms", "area_per_room")

    df["log_living_area"] = np.log(df["living_area"] + 1)
    df["log_estate_size"] = np.log(df["estate_size"] + 1)
    df["log_balcony_size"] = np.log(df["balcony_size"] + 1)
    df["log_garden_size"] = np.log(df["garden_size"] + 1)
    df["log_terrace_size"] = np.log(df["terrace_size"] + 1)
    df["log_loggia_size"] = np.log(df["loggia_size"] + 1)
    df["log_wintergarden_size"] = np.log(df["wintergarden_size"] + 1)
    df["log_distance_nearest_city"] = np.log(df["distance_nearest_city"] + 1)
    df["log_distance_nearest_lake"] = np.log(df["distance_nearest_lake"] + 1)
    df["log_distance_villach"] = np.log(df["distance_villach"] + 1)
    df["log_distance_klagenfurt"] = np.log(df["distance_klagenfurt"] + 1)

    df = df.dropna(subset=["lat", "lon"])
    df[OPTIONAL_FEATURES] = df[OPTIONAL_FEATURES].fillna(0)

    df_features = df[
        [
            "id", "norm_price", "log_price", "ppm2", "log_ppm2", "estate_ratio", "rpm2",
            "ppr", "balcony_ratio", "garden_ratio", "terrace_ratio",
            "loggia_ratio", "wintergarden_ratio", "rooms_per_property",
            "urban_ppm2", "is_urban",
            "distance_nearest_lake", "distance_nearest_city",
            "distance_villach", "distance_klagenfurt",
            "days_since_publish", "area_per_room", "is_efh",
            "is_mfh", "is_lh", "is_villa", "is_dhh", "is_sbc", "is_rh", "is_ab", "is_bh", "is_gh",
            "is_dgw", "is_egw", "is_gc", "is_gw", "is_ms", "is_phw", "is_apt", "is_wg",
            "log_living_area", "log_estate_size", "log_balcony_size", "log_garden_size", "log_terrace_size",
            "log_loggia_size", "log_wintergarden_size", "log_distance_nearest_city", "log_distance_nearest_lake",
            "log_distance_villach", "log_distance_klagenfurt"
        ]
    ]

    return df_features


def printProgressBar(current, total, bar_length=20):
    """Displays a progress bar in the console."""
    progress = current / total
    filled = int(bar_length * progress)

    bar = "=" * filled + ">" + " " * (bar_length - filled - 1)
    percent = int(progress * 100)

    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()

    if current == total:
        print()


def insertFeatureData(rent, buy, conn=None, cur=None):
    """Batches and inserts processed rent and buy features into their respective database tables."""
    logging.info("Insert detail data into database")
    if conn is None or cur is None:
        raise ValueError("Connection and cursor required")

    rent_records = rent.to_dict(orient="records")
    total_batches = (len(rent_records) + PAGES - 1) // PAGES
    print("-------Transfer Rent Data-------")

    for idx, i in enumerate(range(0, len(rent_records), PAGES), 1):
        batch = rent_records[i:i + PAGES]

        try:
            insertFeatures(
                table="rent_features",
                features=batch,
                PAGE_SIZE=PAGES,
                conn=conn,
                cur=cur
            )
            conn.commit()
            logging.info("Inserted %d listings into Rent Data", len(batch))
        except Exception:
            conn.rollback()
            logging.exception("Failed to insert batch into Rent Data")

        printProgressBar(idx, total_batches)

    buy_records = buy.to_dict(orient="records")
    total_batches = (len(buy_records) + PAGES - 1) // PAGES
    print()
    print("-------Transfer Buy Data-------")

    for idx, j in enumerate(range(0, len(buy_records), PAGES), 1):
        batch = buy_records[j:j + PAGES]
        try:
            insertFeatures(
                table="buy_features",
                features=batch,
                PAGE_SIZE=PAGES,
                conn=conn,
                cur=cur
            )
            conn.commit()
            logging.info("Inserted %d listings into Buy Data", len(batch))

        except Exception:
            conn.rollback()
            logging.exception("Failed to insert batch into Buy Data")

        printProgressBar(idx, total_batches)


def deleteRequiredNull(df):
    """Removes rows that are missing essential values for feature calculation."""
    return df[
        df["price"].notna() &
        df["living_area"].notna() &
        df["rooms"].notna() &
        df["property_type"].notna() &
        df["lat"].notna() &
        df["lon"].notna() &
        df["postcode"].notna()
        ]


def filterLowPrice(df, col="price", limit=10):
    """Filters out records with a price below a certain threshold."""
    return df[df[col] >= limit]


def cleanData():
    """Main entry point to load, clean, transform, and save the real estate data."""
    logging.info("Scraping detail listings...")
    conn = get_connection()
    cur = conn.cursor()

    if not conn or not cur:
        logging.error("Connection and / or cursor to db failed")
        return

    df = loadData(conn)
    df = filterLowPrice(df, "price", 10)
    df = quantileElimination(df, "price")

    df_rent = df[df["finance_type"] == "rent"].copy()
    logging.info("Amount rent data: %d", len(df_rent["id"]))
    df_buy = df[df["finance_type"] == "buy"].copy()
    logging.info("Amount buy data: %d", len(df_buy["id"]))

    df_buy = deleteRequiredNull(df_buy)
    df_rent = deleteRequiredNull(df_rent)

    df_rent_features = cleanUp(df_rent)
    df_buy_features = cleanUp(df_buy)

    insertFeatureData(df_rent_features, df_buy_features, conn, cur)

    cur.close()
    conn.close()
