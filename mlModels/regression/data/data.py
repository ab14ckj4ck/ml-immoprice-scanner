from database.db import get_connection
import pandas as pd
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def getData(filter_type: str, filter_val: str, table: str):
    """
    Fetches and merges rental features and listings from the database.
    Args:
        filter_type: filter for specific data category
        filter_val: value to filter for
        table: db table to fetch from

    Returns:
        pd.DataFrame: A dataframe containing selected features and target variables.
    """
    conn = get_connection()
    df_features = None
    if table == "rent_features":
        df_features = pd.read_sql(f"SELECT * FROM rent_features", conn)
    elif table == "buy_features":
        df_features = pd.read_sql(f"SELECT * FROM buy_features", conn)
    else:
        logging.error("Invalid table name to fetch data for clustering from")

    df_listings = pd.read_sql("SELECT * FROM listings", conn)

    df = df_features.merge(df_listings, on="id")
    df = df[df[filter_type] == filter_val]

    df = df[
        [
            "id", "living_area", "estate_size", "rooms", "has_carport", "has_elevator", "has_kitchen",
            "has_garage", "finance_type",
            "has_cellar", "has_parking", "has_closet", "has_balcony", "balcony_size", "has_garden",
            "garden_size",
            "has_terrace", "terrace_size", "has_loggia", "loggia_size", "has_wintergarden", "wintergarden_size",
            "is_oil", "is_bio", "is_electro", "is_pellets", "is_photovoltaik", "is_geothermal", "is_air_heating",
            "is_floor", "is_central", "is_ceiling", "is_oven", "is_infrared", "hwb", "fgee",
            "log_price", "estate_ratio", "rpm2", "balcony_ratio", "garden_ratio", "wintergarden_ratio", "terrace_ratio",
            "rooms_per_property", "distance_nearest_city", "distance_villach", "distance_klagenfurt",
            "distance_nearest_lake",
            "is_urban", "area_per_room", "is_mfh", "is_efh", "is_lh", "is_villa", "is_dhh", "is_sbc", "is_rh", "is_ab",
            "is_bh", "is_gh", "is_dgw", "is_egw", "is_gc", "is_gw", "is_ms", "is_phw", "is_apt", "is_wg",
            "log_living_area", "log_estate_size", "log_balcony_size", "log_garden_size", "log_terrace_size",
            "log_loggia_size", "log_wintergarden_size", "log_distance_nearest_city", "log_distance_nearest_lake",
            "log_distance_villach", "log_distance_klagenfurt"
        ]
    ]
    conn.close()
    return df


def housingTypeSplit(df_X, df_y):
    """
    Splits the dataset into houses and apartments based on specific boolean columns.

    Args:
        df_X (pd.DataFrame): Feature matrix.
        df_y (pd.Series): Target vector.

    Returns:
        tuple: (df_house_X, df_house_y, df_apt_X, df_apt_y)
    """
    house_cols = [
        "is_mfh", "is_efh", "is_lh", "is_villa", "is_dhh",
        "is_sbc", "is_rh", "is_ab", "is_bh", "is_gh"
    ]

    apt_cols = [
        "is_dgw", "is_egw", "is_gc", "is_gw",
        "is_ms", "is_phw", "is_apt", "is_wg"
    ]

    house_mask = df_X[house_cols].any(axis=1)
    apt_mask = df_X[apt_cols].any(axis=1)

    df_house_X = df_X[house_mask]
    df_house_y = df_y[house_mask]

    df_apt_X = df_X[apt_mask]
    df_apt_y = df_y[apt_mask]

    df_apt_X = df_apt_X.drop(columns=house_mask, errors="ignore")
    df_apt_y = df_apt_y.drop(columns=house_mask, errors="ignore")

    df_house_X = df_house_X.drop(columns=apt_mask, errors="ignore")
    df_house_y = df_house_y.drop(columns=apt_mask, errors="ignore")

    return df_house_X, df_house_y, df_apt_X, df_apt_y


def getRegressionData(df):
    """
    Prepares the data for linear regression by dropping redundant columns and
    splitting by housing type.

    Args:
        df (pd.DataFrame): The raw merged dataframe from getData().

    Returns:
        tuple: Split feature matrices and target vectors for houses and apartments. df_house_X, df_house_y, df_apt_X, df_apt_y
    """
    df = df.copy()

    df_y = df["log_price"]

    df_X = df.drop(columns=[
        "id", "log_price", "living_area", "estate_size", "balcony_size",
        "garden_size", "terrace_size", "loggia_size", "wintergarden_size",
        "distance_nearest_city", "distance_villach", "distance_klagenfurt", "distance_nearest_lake",
        "rpm2", "rooms_per_property", "area_per_room", "lat", "lon", "hwb",
    ])

    df_house_X, df_house_y, df_apt_X, df_apt_y = housingTypeSplit(df_X, df_y)

    return df_house_X, df_house_y, df_apt_X, df_apt_y
