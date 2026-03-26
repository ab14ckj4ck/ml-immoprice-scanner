from psycopg2.extras import execute_batch
from utils.enums import Listings, Features


def upsertListings(listings, PAGE_SIZE, conn=None, cur=None):
    """
    Inserts a list of real estate listings into the database.

    Args:
        listings (list): A list of dictionaries containing listing data.
        PAGE_SIZE (int): The number of rows to insert per batch.
        conn: The psycopg2 connection object.
        cur: The psycopg2 cursor object.
    """
    if conn is None or cur is None:
        raise ValueError("Connection and cursor required")

    query = """
            INSERT INTO listings (id,
                                  url,
                                  price,
                                  rent,
                                  safety_deposit,
                                  living_area,
                                  estate_size,
                                  rooms,
                                  postcode,
                                  state,
                                  lat,
                                  lon,
                                  location_quality,
                                  property_type,
                                  finance_type,
                                  published,
                                  scraped_at,
                                  has_carport,
                                  has_elevator,
                                  has_kitchen,
                                  has_garage,
                                  has_cellar,
                                  has_parking,
                                  has_closet,
                                  has_balcony,
                                  balcony_size,
                                  has_garden,
                                  garden_size,
                                  has_terrace,
                                  terrace_size,
                                  has_loggia,
                                  loggia_size,
                                  has_wintergarden,
                                  wintergarden_size,
                                  is_oil,
                                  is_bio,
                                  is_electro,
                                  is_pellets,
                                  is_photovoltaik,
                                  is_geothermal,
                                  is_air_heating,
                                  is_floor,
                                  is_central,
                                  is_ceiling,
                                  is_oven,
                                  is_infrared,
                                  HWB,
                                  HWB_class,
                                  fgEE,
                                  fgEE_class)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET price          = EXCLUDED.price,
                                           rent           = EXCLUDED.rent,
                                           safety_deposit = EXCLUDED.safety_deposit,
                                           scraped_at     = EXCLUDED.scraped_at
            """
    values = [(l[Listings.ID], l[Listings.URL], l[Listings.PRICE], l[Listings.RENT], l[Listings.SAFETY_DEPOSIT],
               l[Listings.LIVING_AREA], l[Listings.ESTATE_SIZE], l[Listings.ROOMS], l[Listings.POSTCODE],
               l[Listings.STATE], l[Listings.LAT], l[Listings.LON], l[Listings.LOCATION_QUALITY],
               l[Listings.PROPERTY_TYPE], l[Listings.FINANCE_TYPE], l[Listings.PUBLISHED], l[Listings.SCRAPED_AT],
               l[Listings.HAS_CARPORT], l[Listings.HAS_ELEVATOR], l[Listings.HAS_KITCHEN], l[Listings.HAS_GARAGE],
               l[Listings.HAS_CELLAR], l[Listings.HAS_PARKING], l[Listings.HAS_CLOSET], l[Listings.HAS_BALCONY],
               l[Listings.BALCONY_SIZE], l[Listings.HAS_GARDEN], l[Listings.GARDEN_SIZE], l[Listings.HAS_TERRACE],
               l[Listings.TERRACE_SIZE], l[Listings.HAS_LOGGIA], l[Listings.LOGGIA_SIZE], l[Listings.HAS_WINTERGARDEN],
               l[Listings.WINTERGARDEN_SIZE], l[Listings.IS_OIL], l[Listings.IS_BIO], l[Listings.IS_ELECTRO],
               l[Listings.IS_PELLETS], l[Listings.IS_PHOTOVOLTAIK], l[Listings.IS_GEOTHERMAL],
               l[Listings.IS_AIR_HEATING], l[Listings.IS_FLOOR], l[Listings.IS_CENTRAL], l[Listings.IS_CEILING],
               l[Listings.IS_OVEN], l[Listings.IS_INFRARED], l[Listings.HWB], l[Listings.HWB_CLASS], l[Listings.FGEE],
               l[Listings.FGEE_CLASS]) for l in listings]
    execute_batch(cur, query, values, page_size=PAGE_SIZE)


def insertHistory(listings, PAGE_SIZE, cur=None):
    """
    Inserts a snapshot of listing prices into the history_listings table.

    Args:
        listings (list): A list of dictionaries containing listing data.
        PAGE_SIZE (int): The number of rows to insert per batch.
        conn: The psycopg2 connection object.
        cur: The psycopg2 cursor object.
    """
    query = """
            INSERT INTO history_listings (id,
                                          price,
                                          rent,
                                          scraped_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id, scraped_at) DO NOTHING
            """
    values = [(l[Listings.ID], l[Listings.PRICE], l[Listings.RENT], l[Listings.SCRAPED_AT],) for l in listings]
    execute_batch(cur, query, values, page_size=PAGE_SIZE)


def updateListings(listings, PAGE_SIZE, conn=None, cur=None):
    query = """
            INSERT INTO listings (id,
                                  price,
                                  rent,
                                  scraped_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET price      = EXCLUDED.price,
                                           rent       = EXCLUDED.rent,
                                           scraped_at = EXCLUDED.scraped_at \
 \
            """
    values = [(l[Listings.ID], l[Listings.PRICE], l[Listings.RENT], l[Listings.SCRAPED_AT],) for l in listings]
    execute_batch(cur, query, values, page_size=PAGE_SIZE)


# noinspection PyUnusedLocal
def insertFeatures(features, PAGE_SIZE, conn=None, cur=None):
    """
    Inserts calculated features into the specified database table.

    Args:
        table (str): The name of the table ('rent_features' or 'buy_features').
        features (list): A list of dictionaries containing feature data.
        PAGE_SIZE (int): The number of rows to insert per batch.
        conn: The psycopg2 connection object.
        cur: The psycopg2 cursor object.
    """
    if conn is None or cur is None:
        raise ValueError("Connection and cursor required - " + table)

    query = """
            INSERT INTO features (id,
                                  log_ppm2,
                                  log_estate_ratio,
                                  location_cluster,
                                  log_distance_to_nearest_city,
                                  log_distance_to_major_city,
                                  log_distance_to_tourism,
                                  log_distance_train_station,
                                  log_count_poi_5km,
                                  log_count_poi_10km,
                                  log_count_poi_25km,
                                  state_vie,
                                  state_noe,
                                  state_ooe,
                                  state_sbg,
                                  state_bgl,
                                  state_stk,
                                  state_ktn,
                                  state_trl,
                                  state_vbg,
                                  log_balcony_size,
                                  log_garden_size,
                                  log_terrace_size,
                                  log_loggia_size,
                                  log_wintergarden_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """
    values = [(f[Features.ID], f[Features.LOG_PPM2], f[Features.LOG_ESTATE_RATIO], f[Features.LOCATION_CLUSTER],
               f[Features.LOG_DISTANCE_TO_NEAREST_CITY], f[Features.LOG_DISTANCE_TO_MAJOR_CITY],
               f[Features.LOG_DISTANCE_TO_TOURISM], f[Features.LOG_DISTANCE_TRAIN_STATION], f[Features.LOG_COUNT_5KM],
               f[Features.LOG_COUNT_10KM], f[Features.LOG_COUNT_25KM], f[Features.STATE_VIE], f[Features.STATE_NOE],
               f[Features.STATE_OOE], f[Features.STATE_SBG], f[Features.STATE_BGL], f[Features.STATE_STK],
               f[Features.STATE_KTN], f[Features.STATE_TRL], f[Features.STATE_VBG], f[Features.LOG_BALCONY_SIZE],
               f[Features.LOG_GARDEN_SIZE], f[Features.LOG_TERRACE_SIZE], f[Features.LOG_LOGGIA_SIZE],
               f[Features.LOG_WINTERGARDEN_SIZE]) for f in features]

    execute_batch(cur, query, values, page_size=PAGE_SIZE)
