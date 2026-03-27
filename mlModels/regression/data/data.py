from database.db import getConnection
from utils.enums import Listings, Features, PropType, Mappings
import pandas as pd
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def getData(filter_type: str, filter_val: str):
    """
    Fetches and merges rental features and listings from the database.
    Args:
        filter_type: filter for specific data category
        filter_val: value to filter for
        table: db table to fetch from

    Returns:
        pd.DataFrame: A dataframe containing selected features and target variables.
    """
    conn = getConnection()
    df_features = pd.read_sql("SELECT * FROM features", conn)
    df_listings = pd.read_sql("SELECT * FROM listings", conn)

    df = df_features.merge(df_listings, on=Listings.ID)
    df = df[df[filter_type] == filter_val]

    df = df[
        [
            Listings.ID, Listings.LIVING_AREA, Listings.ROOMS, Listings.PROPERTY_TYPE, Listings.HAS_CARPORT,
            Listings.HAS_ELEVATOR, Listings.HAS_KITCHEN, Listings.HAS_GARAGE, Listings.HAS_CELLAR,
            Listings.HAS_PARKING, Listings.HAS_CLOSET, Listings.IS_OIL, Listings.IS_BIO, Listings.IS_ELECTRO,
            Listings.IS_PELLETS, Listings.IS_PHOTOVOLTAIK, Listings.IS_GEOTHERMAL, Listings.IS_AIR_HEATING,
            Listings.IS_FLOOR, Listings.IS_CENTRAL, Listings.IS_CEILING, Listings.IS_OVEN, Listings.IS_INFRARED,
            Listings.HWB, Listings.HWB_CLASS, Listings.FGEE, Listings.FGEE_CLASS,

            Features.LOG_PRICE, Features.LOG_ESTATE_RATIO,
            Features.LOG_DISTANCE_TO_NEAREST_CITY, Features.LOG_DISTANCE_TO_MAJOR_CITY,
            Features.LOG_DISTANCE_TO_TOURISM, Features.LOG_DISTANCE_TRAIN_STATION,
            Features.LOG_COUNT_5KM, Features.LOG_COUNT_10KM, Features.LOG_COUNT_25KM,
            Features.STATE_VIE, Features.STATE_NOE, Features.STATE_OOE, Features.STATE_SBG, Features.STATE_BGL,
            Features.STATE_STK, Features.STATE_KTN, Features.STATE_TRL, Features.STATE_VBG,
            Features.LOG_BALCONY_SIZE, Features.LOG_GARDEN_SIZE, Features.LOG_TERRACE_SIZE,
            Features.LOG_LOGGIA_SIZE, Features.LOG_WINTERGARDEN_SIZE
        ]
    ]
    conn.close()
    return df


def getRegressionData(df):
    """
    Prepares the data for linear regression by dropping redundant columns and
    splitting by housing type.

    Args:
        df (pd.DataFrame): The raw merged dataframe from getClusterData().

    Returns:
        tuple: Split feature matrices and target vectors for houses and apartments. df_house_X, df_house_y, df_apt_X, df_apt_y
    """
    df = df.copy()
    df = df.drop(columns=[
        Listings.ID
    ])

    rent_null_rooms_mask = (df[Listings.ROOMS].isnull()) & (df[Listings.PROPERTY_TYPE].isin(Mappings.APARTMENT_COLS))
    df = df[~rent_null_rooms_mask]
    df = df.drop(columns=Mappings.DROP_COLS, errors="ignore")

    house_mask = df[Listings.PROPERTY_TYPE].isin(Mappings.HOUSE_COLS)
    apt_mask = df[Listings.PROPERTY_TYPE].isin(Mappings.APARTMENT_COLS)

    df_house_X = df[house_mask]
    df_house_y = df_house_X[Features.LOG_PRICE]
    df_house_X = df_house_X.drop(columns=Features.LOG_PRICE, errors="ignore")

    df_apt_X = df[apt_mask]
    df_apt_y = df_apt_X[Features.LOG_PRICE]
    df_apt_X = df_apt_X.drop(columns=Features.LOG_PRICE, errors="ignore")

    df_house_X = df_house_X.drop(columns=Listings.PROPERTY_TYPE, errors="ignore")
    df_apt_X = df_apt_X.drop(columns=Listings.PROPERTY_TYPE, errors="ignore")

    return df_house_X, df_house_y, df_apt_X, df_apt_y
