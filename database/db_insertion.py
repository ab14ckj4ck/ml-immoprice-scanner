from psycopg2.extras import execute_batch


def insertListings(listings, PAGE_SIZE, scrape_details=True, conn=None, cur=None):
    """
    Inserts a list of real estate listings into the database.

    Args:
        listings (list): A list of dictionaries containing listing data.
        PAGE_SIZE (int): The number of rows to insert per batch.
        scrape_details (bool): If True, includes detailed features (heating, amenities, etc.).
        conn: The psycopg2 connection object.
        cur: The psycopg2 cursor object.
    """
    if conn is None or cur is None:
        raise ValueError("Connection and cursor required")

    if scrape_details:
        query = """
                INSERT INTO listings (id,
                                      link,
                                      price,
                                      rent,
                                      safety_deposit,
                                      living_area,
                                      estate_size,
                                      rooms,
                                      postcode,
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
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """

        values = [
            (
                l["id"],
                l["link"],
                l["price"],
                l["rent"],
                l["safety_deposit"],
                l["living_area"],
                l["estate_size"],
                l["rooms"],
                l["postcode"],
                l["lat"],
                l["lon"],
                l["location_quality"],
                l["property_type"],
                l["finance_type"],
                l["published"],
                l["scraped_at"],
                l["has_carport"],
                l["has_elevator"],
                l["has_kitchen"],
                l["has_garage"],
                l["has_cellar"],
                l["has_parking"],
                l["has_closet"],
                l["has_balcony"],
                l["balcony_size"],
                l["has_garden"],
                l["garden_size"],
                l["has_terrace"],
                l["terrace_size"],
                l["has_loggia"],
                l["loggia_size"],
                l["has_wintergarden"],
                l["wintergarden_size"],
                l["oil"],
                l["bio"],
                l["electro"],
                l["pellets"],
                l["photovoltaik"],
                l["geothermal"],
                l["air_heating"],
                l["floor_heating"],
                l["central_heating"],
                l["ceiling_heating"],
                l["oven_heating"],
                l["infrared_heating"],
                l["hwb"],
                l["hwb_class"],
                l["fgee"],
                l["fgee_class"],
            )
            for l in listings
        ]
    else:
        query = """
                INSERT INTO listings (id,
                                      link,
                                      price,
                                      rent,
                                      safety_deposit,
                                      living_area,
                                      estate_size,
                                      rooms,
                                      postcode,
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
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """

        values = [
            (
                l["id"],
                l["link"],
                l["price"],
                l["rent"],
                l["safety_deposit"],
                l["living_area"],
                l["estate_size"],
                l["rooms"],
                l["postcode"],
                l["lat"],
                l["lon"],
                l["location_quality"],
                l["property_type"],
                l["finance_type"],
                l["published"],
                l["scraped_at"],
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
            for l in listings
        ]
    execute_batch(cur, query, values, page_size=PAGE_SIZE)


def insertFeatures(table, features, PAGE_SIZE, conn=None, cur=None):
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

    query = ""
    if table == "rent_features":
        query = """
                INSERT INTO rent_features (id, norm_price, log_price, ppm2, log_ppm2, urban_ppm2, estate_ratio, rpm2,
                                           ppr, balcony_ratio, garden_ratio, loggia_ratio, wintergarden_ratio,
                                           terrace_ratio, rooms_per_property, distance_nearest_city, distance_villach,
                                           distance_klagenfurt, distance_nearest_lake, is_urban,
                                           days_since_publish, area_per_room, is_mfh, is_efh, is_lh, is_villa, is_dhh,
                                           is_sbc, is_rh, is_ab, is_bh, is_gh, is_dgw, is_egw, is_gc, is_gw, is_ms,
                                           is_phw, is_apt, is_wg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """
    elif table == "buy_features":
        query = """
                INSERT INTO buy_features (id, norm_price, log_price, ppm2, log_ppm2, urban_ppm2, estate_ratio, rpm2,
                                           ppr, balcony_ratio, garden_ratio, loggia_ratio, wintergarden_ratio,
                                           terrace_ratio, rooms_per_property, distance_nearest_city, distance_villach,
                                           distance_klagenfurt, distance_nearest_lake, is_urban,
                                           days_since_publish, area_per_room, is_mfh, is_efh, is_lh, is_villa, is_dhh,
                                           is_sbc, is_rh, is_ab, is_bh, is_gh, is_dgw, is_egw, is_gc, is_gw, is_ms,
                                           is_phw, is_apt, is_wg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """

    else:
        raise ValueError("Query failed features")

    values = [(
        f["id"],
        f["norm_price"],
        f["log_price"],
        f["ppm2"],
        f["log_ppm2"],
        f["urban_ppm2"],
        f["estate_ratio"],
        f["rpm2"],
        f["ppr"],
        f["balcony_ratio"],
        f["garden_ratio"],
        f["loggia_ratio"],
        f["wintergarden_ratio"],
        f["terrace_ratio"],
        f["rooms_per_property"],
        f["distance_nearest_city"],
        f["distance_villach"],
        f["distance_klagenfurt"],
        f["distance_nearest_lake"],
        f["is_urban"],
        f["days_since_publish"],
        f["area_per_room"],
        f["is_mfh"],
        f["is_efh"],
        f["is_lh"],
        f["is_villa"],
        f["is_dhh"],
        f["is_sbc"],
        f["is_rh"],
        f["is_ab"],
        f["is_bh"],
        f["is_gh"],
        f["is_dgw"],
        f["is_egw"],
        f["is_gc"],
        f["is_gw"],
        f["is_ms"],
        f["is_phw"],
        f["is_apt"],
        f["is_wg"]
    ) for f in features
    ]
    execute_batch(cur, query, values, page_size=PAGE_SIZE)
