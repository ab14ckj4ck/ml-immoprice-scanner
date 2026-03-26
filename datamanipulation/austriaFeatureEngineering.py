from database.db import getConnection
from database.db_insertion import insertFeatures
from datamanipulation.loaders import loadLocationData
from data.enums import *

import numpy as np
import pandas as pd
import logging

TARGET_CITY = "city"
TARGET_MAJOR_CITY = "major_city"
TARGET_STATION = "station"
TARGET_POI = "poi"
URBAN_THRESHOLD = 25
PAGES = 20



logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def loadData(conn):
    """
    Loads all listing data from the database.

    Args:
        conn: Database connection object.
    Returns:
        pd.DataFrame: DataFrame containing all listings.
    """
    return pd.read_sql("SELECT * FROM listings", conn)

def quantileElimination(df, col, q_low_val=0.05, q_high_val=0.95):
    """
    Removes outliers from a DataFrame based on quantiles for a specific column.

    Args:
        df: Input DataFrame.
        col: Column name to filter by.
        q_low_val: Lower quantile threshold.
        q_high_val: Upper quantile threshold.
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    df = df.copy()
    q_low = df[col].quantile(q_low_val)
    q_high = df[col].quantile(q_high_val)
    return df[(df[col] >= q_low) & (df[col] <= q_high)]

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points on Earth in kilometers.
    """
    R = 6371.0

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = np.sin(d_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c

def findNearestPointOfInterest(df, pois):
    """
    For each listing, finds the distance to the nearest POI and counts POIs within radii.

    Args:
        df: DataFrame of listings with LAT/LON.
        pois: List of POI objects/dicts with LAT/LON.
    Returns:
        tuple: (min_distances, counts_5km, counts_10km, counts_25km)
    """
    n = len(df)

    count_5 = np.zeros(n)
    count_10 = np.zeros(n)
    count_25 = np.zeros(n)

    distances = []

    for poi in pois:
        d = haversine(
            df[Listings.LAT].values,
            df[Listings.LON].values,
            poi[Listings.LAT],
            poi[Listings.LON]
        )
        count_5 += (d < 5)
        count_10 += (d < 10)
        count_25 += (d < 25)
        distances.append(d)

    distances = np.vstack(distances)
    min_dist = distances.min(axis=0)

    return min_dist, count_5, count_10, count_25


def setStates(df, df_features):
    """
    Applies one-hot encoding for Austrian states based on the STATE_MAPPING.
    """
    for state, col in Mappings.STATE_MAPPING.items():
        df_features[col] = (df[Listings.STATE] == state).astype(int)

    return df_features


def engineerFeatures():
    """
    Main pipeline for feature engineering. Loads raw data, calculates spatial and
    numerical features, and inserts the processed features back into the database.
    """
    conn = getConnection()
    cur = conn.cursor()

    df = loadData(conn)
    df_features = pd.DataFrame()

    # prepare data
    df = quantileElimination(df, Listings.PRICE, 0.05, 0.95)
    df_features[Features.ID] = df[Listings.ID]

    # calc features
    df_features[Features.LOG_PPM2] = np.log(df[Listings.PRICE] / df[Listings.LIVING_AREA] + 1)
    df_features[Features.LOG_ESTATE_RATIO] = np.log(df[Listings.ESTATE_SIZE] / df[Listings.LIVING_AREA] + 1)

    df_features[Features.LOCATION_CLUSTER] = -1 # placeholder

    # calc distance features
    cities = loadLocationData(path=DataFiles.CITIES_FILE, target=TARGET_CITY)
    poi, delete_5, delete_10, delete_25 = findNearestPointOfInterest(df, cities)
    df_features[Features.LOG_DISTANCE_TO_NEAREST_CITY] = np.log(poi + 1)

    major_cities = loadLocationData(path=DataFiles.MAJOR_CITIES_FILE, target=TARGET_MAJOR_CITY)
    poi, delete_5, delete_10, delete_25 = findNearestPointOfInterest(df, major_cities)
    df_features[Features.LOG_DISTANCE_TO_MAJOR_CITY] = np.log(poi + 1)

    train_stations = loadLocationData(path=DataFiles.TRAIN_STATIONS_FILE, target=TARGET_STATION)
    poi, delete_5, delete_10, delete_25 = findNearestPointOfInterest(df, train_stations)
    df_features[Features.LOG_DISTANCE_TRAIN_STATION] = np.log(poi + 1)

    pois = loadLocationData(path=DataFiles.POI_FILE, target=TARGET_POI)
    poi, count_5km, count_10km, count_25km = findNearestPointOfInterest(df, pois)
    df_features[Features.LOG_DISTANCE_TO_TOURISM] = np.log(pois + 1)
    df_features[Features.LOG_COUNT_5KM] = np.log(count_5km + 1)
    df_features[Features.LOG_COUNT_10KM] = np.log(count_10km + 1)
    df_features[Features.LOG_COUNT_25KM] = np.log(count_25km + 1)

    # set state one-hot encoding
    df_features = setStates(df, df_features)

    # set log extra sizes
    df_features[Features.LOG_BALCONY_SIZE] = np.log(df[Listings.BALCONY_SIZE] + 1)
    df_features[Features.LOG_GARDEN_SIZE] = np.log(df[Listings.GARDEN_SIZE] + 1)
    df_features[Features.LOG_TERRACE_SIZE] = np.log(df[Listings.TERRACE_SIZE] + 1)
    df_features[Features.LOG_LOGGIA_SIZE] = np.log(df[Listings.LOGGIA_SIZE] + 1)
    df_features[Features.LOG_WINTERGARDEN_SIZE] = np.log(df[Listings.WINTERGARDEN_SIZE] + 1)

    insertFeatures(df_features, PAGES, conn, cur)
