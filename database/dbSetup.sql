CREATE TABLE listings (
                          id TEXT PRIMARY KEY,
                          link TEXT,

                          price FLOAT,
                          rent FLOAT,
                          safety_deposit FLOAT,

                          living_area FLOAT,
                          estate_size FLOAT,
                          rooms INT,

                          postcode TEXT,

                          lat FLOAT,
                          lon FLOAT,

                          location_quality FLOAT,

                          property_type TEXT,

                          finance_type TEXT,

                          published BIGINT,
                          scraped_at DATE DEFAULT CURRENT_DATE,

    -- accomodations
                          has_carport INT,
                          has_elevator INT,
                          has_kitchen INT,
                          has_garage INT,
                          has_cellar INT,
                          has_parking INT,
                          has_closet INT,
                          has_balcony INT,
                          balcony_size FLOAT,
                          has_garden INT,
                          garden_size FLOAT,
                          has_terrace INT,
                          terrace_size FLOAT,
                          has_loggia INT,
                          loggia_size FLOAT,
                          has_wintergarden INT,
                          wintergarden_size FLOAT,

    --heating source
                          is_oil INT,
                          is_bio INT,
                          is_electro INT,
                          is_pellets INT,
                          is_photovoltaik INT,
                          is_geothermal INT,
                          is_air_heating INT,

    --heating type
                          is_floor INT,
                          is_central INT,
                          is_ceiling INT,
                          is_oven INT,
                          is_infrared INT,

                          HWB FLOAT,
                          HWB_class INT,
                          fgEE FLOAT,
                          fgEE_class INT
);

CREATE TABLE rent_features (
                               id TEXT PRIMARY KEY REFERENCES listings(id),

                               norm_price FLOAT,
                               log_price FLOAT,

                               ppm2 FLOAT, --price per m²
                               log_ppm2 FLOAT, --LN(ppm2)
                               urban_ppm2 FLOAT, --ppm2 * is_urban
                               estate_ratio FLOAT, --estateSize / livingArea
                               rpm2 FLOAT, --rooms per m²
                               ppr FLOAT, -- price / rooms
                               balcony_ratio FLOAT, -- balcony / living area
                               garden_ratio FLOAT, -- garden / living area
                               loggia_ratio FLOAT, -- loggia / living area
                               wintergarden_ratio FLOAT, -- wintergarden / living area
                               terrace_ratio FLOAT, -- terrace / living area
                               rooms_per_property FLOAT, -- rooms / estate_size + 1

                               distance_nearest_city FLOAT,
                               distance_villach FLOAT,
                               distance_klagenfurt FLOAT,
                               distance_nearest_lake FLOAT,

                               is_urban INT,

                               is_house INT,
                               is_apartment INT
);

CREATE TABLE buy_features (
                              id TEXT PRIMARY KEY REFERENCES listings(id),

                              norm_price FLOAT,
                              log_price FLOAT,

                              ppm2 FLOAT, --price per m²
                              log_ppm2 FLOAT, --LN(ppm2)
                              urban_ppm2 FLOAT, --ppm2 * is_urban
                              estate_ratio FLOAT, --estateSize / livingArea
                              rpm2 FLOAT, --rooms per m²
                              ppr FLOAT, -- price / rooms
                              balcony_ratio FLOAT, -- balcony / living area
                              garden_ratio FLOAT, -- garden / living area
                              loggia_ratio FLOAT, -- loggia / living area
                              wintergarden_ratio FLOAT, -- wintergarden / living area
                              terrace_ratio FLOAT, -- terrace / living area
                              rooms_per_property FLOAT, -- rooms / estate_size + 1

                              distance_nearest_city FLOAT,
                              distance_villach FLOAT,
                              distance_klagenfurt FLOAT,
                              distance_nearest_lake FLOAT,

                              is_urban INT,

                              is_house INT,
                              is_apartment INT
);
