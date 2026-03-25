CREATE TABLE listings
(
    id                TEXT PRIMARY KEY,
    link              TEXT,

    price             FLOAT,
    rent              FLOAT,
    safety_deposit    FLOAT,

    living_area       FLOAT,
    estate_size       FLOAT,
    rooms             INT,

    postcode          TEXT,
    state             TEXT,

    lat               FLOAT,
    lon               FLOAT,

    location_quality  FLOAT,

    property_type     TEXT,

    finance_type      TEXT,

    published         BIGINT,
    scraped_at        DATE DEFAULT CURRENT_DATE,

    -- accomodations
    has_carport       INT,
    has_elevator      INT,
    has_kitchen       INT,
    has_garage        INT,
    has_cellar        INT,
    has_parking       INT,
    has_closet        INT,
    has_balcony       INT,
    balcony_size      FLOAT,
    has_garden        INT,
    garden_size       FLOAT,
    has_terrace       INT,
    terrace_size      FLOAT,
    has_loggia        INT,
    loggia_size       FLOAT,
    has_wintergarden  INT,
    wintergarden_size FLOAT,

    --heating source
    is_oil            INT,
    is_bio            INT,
    is_electro        INT,
    is_pellets        INT,
    is_photovoltaik   INT,
    is_geothermal     INT,
    is_air_heating    INT,

    --heating type
    is_floor          INT,
    is_central        INT,
    is_ceiling        INT,
    is_oven           INT,
    is_infrared       INT,

    HWB               FLOAT,
    HWB_class         INT,
    fgEE              FLOAT,
    fgEE_class        INT
);

CREATE TABLE history_listings
(
    hist_id        SERIAL PRIMARY KEY,
    id             TEXT REFERENCES listings (id),

    price          FLOAT,
    rent           FLOAT,
    safety_deposit FLOAT,

    scraped_at     DATE
);

CREATE TABLE features
(
    log_ppm2                     FLOAT,
    log_estate_ratio             FLOAT,

    location_cluster             FLOAT,

    log_distance_to_nearest_city FLOAT,
    log_distance_to_major_city   FLOAT,
    log_distance_to_tourism      FLOAT,
    log_distance_train_station   FLOAT,

    -- States
    state_vie                    INT,
    state_noe                    INT,
    state_ooe                    INT,
    state_sbg                    INT,
    state_bgl                    INT,
    state_stk                    INT,
    state_ktn                    INT,
    state_trl                    INT,
    state_vbg                    INT,

    log_balcony_size             FLOAT,
    log_garden_size              FLOAT,
    log_terrace_size             FLOAT,
    log_loggia_size              FLOAT,
    log_wintergarden_size        FLOAT
);

CREATE TABLE rent_features
(
    id                        TEXT PRIMARY KEY REFERENCES listings (id),

    norm_price                FLOAT,
    log_price                 FLOAT,

    ppm2                      FLOAT, --price per m²
    log_ppm2                  FLOAT, --LN(ppm2)
    urban_ppm2                FLOAT, --ppm2 * is_urban
    estate_ratio              FLOAT, --estateSize / livingArea
    rpm2                      FLOAT, --rooms per m²
    ppr                       FLOAT, -- price / rooms
    balcony_ratio             FLOAT, -- balcony / living area
    garden_ratio              FLOAT, -- garden / living area
    loggia_ratio              FLOAT, -- loggia / living area
    wintergarden_ratio        FLOAT, -- wintergarden / living area
    terrace_ratio             FLOAT, -- terrace / living area
    rooms_per_property        FLOAT, -- rooms / estate_size + 1

    distance_nearest_city     FLOAT,
    distance_villach          FLOAT,
    distance_klagenfurt       FLOAT,
    distance_nearest_lake     FLOAT,

    is_urban                  INT,

    days_since_publish        FLOAT,
    area_per_room             FLOAT,

    -- houses
    is_mfh                    INT,   -- multifamily house
    is_efh                    INT,   -- single family house
    is_lh                     INT,   -- Landhaus
    is_villa                  INT,
    is_dhh                    INT,   -- Half double house
    is_sbc                    INT,   -- castle or charlet
    is_rh                     INT,   -- row house
    is_ab                     INT,   -- mountain cabin
    is_bh                     INT,   -- farmer house
    is_gh                     INT,   -- cooperative house

    -- apartments
    is_dgw                    INT,   -- roof floor apt
    is_egw                    INT,   -- first floor apt
    is_gc                     INT,   -- garconniere apt
    is_gw                     INT,   -- cooperative apt
    is_ms                     INT,   -- maisonette
    is_phw                    INT,   -- penthouse apt
    is_apt                    INT,   -- apartment
    is_wg                     INT,   -- room / WG

    -- log data
    log_living_area           FLOAT,
    log_estate_size           FLOAT,
    log_balcony_size          FLOAT,
    log_garden_size           FLOAT,
    log_terrace_size          FLOAT,
    log_loggia_size           FLOAT,
    log_wintergarden_size     FLOAT,
    log_distance_nearest_city FLOAT,
    log_distance_nearest_lake FLOAT,
    log_distance_villach      FLOAT,
    log_distance_klagenfurt   FLOAT
);

CREATE TABLE buy_features
(
    id                        TEXT PRIMARY KEY REFERENCES listings (id),

    norm_price                FLOAT,
    log_price                 FLOAT,

    ppm2                      FLOAT, --price per m²
    log_ppm2                  FLOAT, --LN(ppm2)
    urban_ppm2                FLOAT, --ppm2 * is_urban
    estate_ratio              FLOAT, --estateSize / livingArea
    rpm2                      FLOAT, --rooms per m²
    ppr                       FLOAT, -- price / rooms
    balcony_ratio             FLOAT, -- balcony / living area
    garden_ratio              FLOAT, -- garden / living area
    loggia_ratio              FLOAT, -- loggia / living area
    wintergarden_ratio        FLOAT, -- wintergarden / living area
    terrace_ratio             FLOAT, -- terrace / living area
    rooms_per_property        FLOAT, -- rooms / estate_size + 1

    distance_nearest_city     FLOAT,
    distance_villach          FLOAT,
    distance_klagenfurt       FLOAT,
    distance_nearest_lake     FLOAT,

    is_urban                  INT,

    days_since_publish        FLOAT,
    area_per_room             FLOAT,

    -- houses
    is_bungalow               INT,
    is_mfh                    INT,   -- multifamily house
    is_efh                    INT,   -- single family house
    is_lh                     INT,   -- Landhaus
    is_villa                  INT,
    is_dhh                    INT,   -- Half double house
    is_sbc                    INT,   -- castle or charlet
    is_rh                     INT,   -- row house
    is_ab                     INT,   -- mountain cabin
    is_bh                     INT,   -- farmer house
    is_gh                     INT,   -- cooperative house

    -- apartments
    is_dgw                    INT,   -- roof floor apt
    is_egw                    INT,   -- first floor apt
    is_gc                     INT,   -- garconniere apt
    is_gw                     INT,   -- cooperative apt
    is_ms                     INT,   -- maisonette
    is_phw                    INT,   -- penthouse apt
    is_apt                    INT,   -- apartment
    is_wg                     INT,   -- room / WG

    -- log data
    log_living_area           FLOAT,
    log_estate_size           FLOAT,
    log_balcony_size          FLOAT,
    log_garden_size           FLOAT,
    log_terrace_size          FLOAT,
    log_loggia_size           FLOAT,
    log_wintergarden_size     FLOAT,
    log_distance_nearest_city FLOAT,
    log_distance_nearest_lake FLOAT,
    log_distance_villach      FLOAT,
    log_distance_klagenfurt   FLOAT
);

CREATE TABLE history_listings
(
    id         TEXT,
    price      NUMERIC,
    rent       NUMERIC,
    scraped_at DATE,
    UNIQUE (id, scraped_at)
);
