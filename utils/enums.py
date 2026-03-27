class Listings:
    ID = "id"
    URL = "url"
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
    HWB = "hwb"
    HWB_CLASS = "hwb_class"
    FGEE = "fgee"
    FGEE_CLASS = "fgee_class"


class HistoryListings:
    HIST_ID = "hist_id"


class Features:
    ID = "id"
    LOG_PRICE = "log_price"
    LOG_ESTATE_RATIO = "log_estate_ratio"
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


class DataFiles:
    CITIES_FILE = "data/cities.xml"
    MAJOR_CITIES_FILE = "data/major-cities.xml"
    TRAIN_STATIONS_FILE = "data/train-stations.xml"
    POI_FILE = "data/pois.xml"


class ScraperValues:
    STATES = ("kaernten", "wien", "steiermark", "oberoesterreich", "niederoesterreich", "burgenland", "salzburg", "tirol", "vorarlberg")  # TODO implement buttons for this values to GUI
    MAX_SLEEP_TIME = 15
    MIN_SLEEP_TIME = 0.5
    ENERGY_MAP = {"A++": 9, "A+": 8, "A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}
    BATCH_SIZE = 20
    PAGE_SIZE = 20


class FEValues:
    TARGET_CITY = "city"
    TARGET_MAJOR_CITY = "major_city"
    TARGET_STATION = "station"
    TARGET_POI = "poi"
    PAGES = 20


class LoaderValues:
    VALID_IMMO_TYPES = ("house", "apartment", "projects")
    VALID_FIN_TYPES = ("rent", "buy")  # TODO implement "project" handling
    LINK = "link"
    CATEGORY = "category"
    IMMO = "immo"
    TYPE = "type"
    URL = "url"
    FIN_TYPE = "fin_type"
    NAME = "name"
    LAT = "lat"
    LON = "lon"


class TestParam:
    TEST_SOURCE_1 = True
    TEST_SOURCE_1_DETAIL = True
    TEST_CLEAN = True
    TEST_LOADERS = True


# TODO Implement runModel again
class ModelParam:
    REGRESSION = False
    CV_FOLDS = 5
    HOUSES = True
    APARTMENTS = True
    RENT = True
    BUY = True


class PropType:
    ALM_BERG = "Almhütte/Berghütte"
    FARMHOUSE = "Bauernhaus"
    BUNGALOW = "Bungalow"
    SEMI_DETACHED = "Doppelhaushälfte"
    SINGLE_FAMILY = "Einfamilienhaus"
    MULTI_FAMILY = "Mehrfamilienhaus"
    COOP_HOUSE = "Genossenschaftshaus"
    COUNTRY_HOUSE = "Landhaus"
    TERRACED = "Reihenhaus"
    SHELL_CONSTRUCTION = "Rohbau"
    CASTLE_CHALET = "Schloss/Burg/Chalet"
    VILLA = "Villa"

    ROOF_APARTMENT = "Dachgeschosswohnung"
    GROUND_APARTMENT = "Erdgeschoßwohnung"
    GARCONNIERE = "Garconniere"
    COOP_APARTMENT = "Genossenschaftswohnung"
    LOFT_STUDIO = "Loft/Studio"
    MAISONETTE = "Maisonette"
    PENTHOUSE = "Penthousewohnung"
    APARTMENT = "Wohnung"
    ROOM_SHARED = "Zimmer/WG"

    ATTIC_RAW = "Rohdachboden"
    GARDEN_HOUSE = "Gartenhaus"
    OTHER = "Sonstige"

class Mappings:
    STATE_MAPPING = {"kaernten": Features.STATE_KTN, "wien": Features.STATE_VIE, "steiermark": Features.STATE_STK,
        "niederoesterreich": Features.STATE_NOE, "oberoesterreich": Features.STATE_OOE, "burgendland": Features.STATE_BGL,
        "salzburg": Features.STATE_SBG, "tirol": Features.STATE_TRL, "vorarlberg": Features.STATE_VBG}

    OPTIONAL_DATA = ["has_carport", "has_elevator", "has_kitchen", "has_garage", "has_cellar", "has_parking",
        "has_closet", "has_balcony", "has_garden", "has_terrace", "has_loggia", "has_wintergarden", "balcony_size",
        "garden_size", "terrace_size", "loggia_size", "wintergarden_size", "hwb", "hwb_class", "fgee", "fgee_class"]

    HOUSE_COLS = [
        PropType.MULTI_FAMILY, PropType.SINGLE_FAMILY, PropType.COUNTRY_HOUSE, PropType.VILLA, PropType.SEMI_DETACHED,
        PropType.CASTLE_CHALET, PropType.TERRACED, PropType.ALM_BERG, PropType.FARMHOUSE, PropType.BUNGALOW,
        PropType.COOP_HOUSE
    ]

    APARTMENT_COLS = [
        PropType.ROOF_APARTMENT, PropType.GROUND_APARTMENT, PropType.GARCONNIERE, PropType.COOP_APARTMENT,
        PropType.LOFT_STUDIO, PropType.MAISONETTE, PropType.PENTHOUSE, PropType.APARTMENT,
        PropType.ROOM_SHARED
    ]

    DROP_COLS = [
        Listings.HWB, Listings.HWB_CLASS, Listings.FGEE, Listings.FGEE_CLASS, Features.LOG_ESTATE_RATIO
    ]
