from database.db import getConnection
from database.db_insertion import insertFeatures
from datamanipulation.loaders import loadLocationData
from data.enums import Listings, Features, Mappings
from geopy.geocoder import Nominatim

import numpy as np
import logging

TARGET_CITY = "city"
TARGET_STATION = "station"
TARGET_POI = "poi"
URBAN_THRESHOLD = 25
PAGES = 20



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

def haversine(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance between two points on Earth in kilometers."""
    R = 6371.0

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = np.sin(d_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c

def findNearestPointOfInterest(df, points_of_interest):
    distances = []

    for poi in points_of_interest:
        d = haversine(df[Listings.LAT], df[Listings.LON], poi[Listings.LAT], poi[Listings.LON])
        distances.append(d)

    distances = np.vstack(distances)

    return distances.min(axis=0)


def setStates(df, df_features):
    for state, col in Mappings.STATE_MAPPING.items():
        df_features[col] = (df[Listings.STATE] == state).astype(int)

    return df_features


def engineerFeatures():
    conn = getConnection()
    cur = conn.cursor()

    df = loadData(conn)
    df_features = pd.DataFrame()

    # prepare data
    df = quantileElimination(df, Listings.PRICE, 0.05, 0.95)


    # calc features
    df_features[Features.LOG_PPM2] = np.log(df[Listings.PRICE] / df[Listings.LIVING_AREA] + 1)
    df_features[Features.LOG_ESTATE_RATIO] = np.log(df[Listings.ESTATE_SIZE] / df[Listings.LIVING_AREA] + 1)

    df_features[Features.LOCATION_CLUSTER] = -1 # placeholder

    # calc distance features
    cities = loadLocationData(path=CITIES_FILE, target=TARGET_CITY)
    df_features[Features.LOG_DISTANCE_TO_NEAREST_CITY] = np.log(findNearestPointOfInterest(df, cities) + 1)

    major_cities = loadLocationData(path=MAJOR_CITIES_FILE, target=TARGET_CITY)
    df_features[Features.LOG_DISTANCE_TO_MAJOR_CITY] = np.log(findNearestPointOfInterest(df, major_cities) + 1)

    train_stations = loadLocationData(path=TRAIN_STATIONS_FILE, target=TARGET_STATION)
    df_features[Features.LOG_DISTANCE_TRAIN_STATION] = np.log(findNearestPointOfInterest(df, train_stations) + 1)

    pois = loadLocationData(path=POI_FILE, target=TARGET_POI)
    df_features[Features.LOG_DISTANCE_TO_TOURISM] = np.log(findNearestPointOfInterest(df, pois) + 1)

    # set state one-hot encoding
    df_features = setStates(df, df_features)

    # set log extra sizes
    df_features[Features.LOG_BALCONY_SIZE] = np.log(df[Listings.BALCONY_SIZE] + 1)
    df_features[Features.LOG_GARDEN_SIZE] = np.log(df[Listings.GARDEN_SIZE] + 1)
    df_features[Features.LOG_TERRACE_SIZE] = np.log(df[Listings.TERRACE_SIZE] + 1)
    df_features[Features.LOG_LOGGIA_SIZE] = np.log(df[Listings.LOGGIA_SIZE] + 1)
    df_features[Features.LOG_WINTERGARDEN_SIZE] = np.log(df[Listings.WINTERGARDEN_SIZE] + 1)

    insertFeatures(df_features, PAGES, conn, cur)








