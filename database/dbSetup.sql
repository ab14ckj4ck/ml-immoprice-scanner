CREATE TABLE listings
(
    id                TEXT PRIMARY KEY,
    url               TEXT,

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
    id                           TEXT PRIMARY KEY REFERENCES listings (id),
    ppm2                         FLOAT,
    log_estate_ratio             FLOAT,

    log_distance_to_nearest_city FLOAT,
    log_distance_to_major_city   FLOAT,
    log_distance_to_tourism      FLOAT,
    log_distance_train_station   FLOAT,
    log_count_poi_5km            FLOAT,
    log_count_poi_10km           FLOAT,
    log_count_poi_25km           FLOAT,

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

CREATE TABLE history_listings
(
    id         TEXT,
    price      NUMERIC,
    rent       NUMERIC,
    scraped_at DATE,
    UNIQUE (id, scraped_at)
);
