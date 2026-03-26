"""
This module defines enumeration-like classes and constants used throughout the
immopreis-regression project to ensure consistent referencing of database columns,
feature names, and file paths.
"""

class Listings:
    """Column names for the raw listings data."""
    ID = "id"
    LINK = "link"
    PRICE = "price"
    RENT = "rent"
    SAFETY_DEPOSIT = "safety_deposit"
    LIVING_AREA = "living_area"
    ESTATE_SIZE = "estate_size"
    ROOMS = "rooms"
    POSTCODE = "postcode"
    STATE = "state"
    LAT = "lat"
    LON = "lon"
    LOCATION_QUALITY = "location_quality"
    PROPERTY_TYPE = "property_type"
    FINANCE_TYPE = "finance_type"
    PUBLISHED = "published"
    SCRAPED_AT = "scraped_at"
    HAS_CARPORT = "has_carport"
    HAS_ELEVATOR = "has_elevator"
    HAS_KITCHEN = "has_kitchen"
    HAS_GARAGE = "has_garage"
    HAS_CELLAR = "has_cellar"
    HAS_PARKING = "has_parking"
    HAS_CLOSET = "has_closet"
    HAS_BALCONY = "has_balcony"
    BALCONY_SIZE = "balcony_size"
    HAS_GARDEN = "has_garden"
    GARDEN_SIZE = "garden_size"
    HAS_TERRACE = "has_terrace"
    TERRACE_SIZE = "terrace_size"
    HAS_LOGGIA = "has_loggia"
    LOGGIA_SIZE = "loggia_size"
    HAS_WINTERGARDEN = "has_wintergarden"
    WINTERGARDEN_SIZE = "wintergarden_size"
    IS_OIL = "is_oil"
    IS_BIO = "is_bio"
    IS_ELECTRO = "is_electro"
    IS_PELLETS = "is_pellets"
    IS_PHOTOVOLTAIK = "is_photovoltaik"
    IS_GEOTHERMAL = "is_geothermal"
    IS_AIR_HEATING = "is_air_heating"
    IS_FLOOR = "is_floor"
    IS_CENTRAL = "is_central"
    IS_CEILING = "is_ceiling"
    IS_OVEN = "is_oven"
    IS_INFRARED = "is_infrared"
    HWB = "HWB"
    HWB_CLASS = "HWB_class"
    FGE = "fgEE"
    FGE_CLASS = "fgEE_class"


class HistoryListings:
    """Column names for historical listing tracking."""
    HIST_ID = "hist_id"


class Features:
    """Column names for engineered features used in the regression model."""
    ID = "id"
    LOG_PPM2 = "log_ppm2"
    LOG_ESTATE_RATIO = "log_estate_ratio"
    LOCATION_CLUSTER = "location_cluster"
    LOG_DISTANCE_TO_NEAREST_CITY = "log_distance_to_nearest_city"
    LOG_DISTANCE_TO_MAJOR_CITY = "log_distance_to_major_city"
    LOG_DISTANCE_TO_TOURISM = "log_distance_to_tourism"
    LOG_DISTANCE_TRAIN_STATION = "log_distance_train_station"
    LOG_COUNT_5KM = "log_count_poi_5km"
    LOG_COUNT_10KM = "log_count_poi_10km"
    LOG_COUNT_25KM = "log_count_poi_25km"
    STATE_VIE = "state_vie"
    STATE_NOE = "state_noe"
    STATE_OOE = "state_ooe"
    STATE_SBG = "state_sbg"
    STATE_BGL = "state_bgl"
    STATE_STK = "state_stk"
    STATE_KTN = "state_ktn"
    STATE_TRL = "state_trl"
    STATE_VBG = "state_vbg"
    LOG_BALCONY_SIZE = "log_balcony_size"
    LOG_GARDEN_SIZE = "log_garden_size"
    LOG_TERRACE_SIZE = "log_terrace_size"
    LOG_LOGGIA_SIZE = "log_loggia_size"
    LOG_WINTERGARDEN_SIZE = "log_wintergarden_size"


class Mappings:
    """Mappings for data normalization and lists of optional fields."""
    STATE_MAPPING = {
        "kaernten": "state_ktn",
        "wien": "state_vie",
        "steiermark": "state_stk",
        "niederoesterreich": "state_noe",
        "oberoesterreich": "state_ooe",
        "burgendland": "state_bgl",
        "salzburg": "state_sbg",
        "tirol": "state_trl",
        "vorarlberg": "state_vbg"
    }

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

class DataFiles:
    """File paths for external data sources used in feature engineering."""
    CITIES_FILE = "data/cities.xml"
    MAJOR_CITIES_FILE = "data/major-cities.xml"
    TRAIN_STATIONS_FILE = "data/train-stations.xml"
    POI_FILE = "data/pois.xml"
