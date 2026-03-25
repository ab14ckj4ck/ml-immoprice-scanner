def getColumnList():
    return ['id', 'living_area', 'estate_size', 'rooms', 'lat', 'lon', 'postcode', 'has_carport',
            'has_elevator', 'has_kitchen', 'has_garage',
            'has_cellar', 'has_parking', 'has_closet', 'has_balcony', 'balcony_size',
            'has_garden', 'garden_size', 'has_terrace', 'terrace_size', 'has_loggia',
            'loggia_size', 'has_wintergarden',
            'wintergarden_size', 'is_oil', 'is_bio', 'is_electro', 'is_pellets',
            'is_photovoltaik', 'is_geothermal',
            'is_air_heating',
            'is_floor', 'is_central',
            'is_ceiling', 'is_oven', 'is_infrared', 'hwb', 'hwb_class', 'fgee',
            'fgee_class', 'is_mfh',
            'is_efh', 'is_lh', 'is_villa',
            'is_dhh', 'is_sbc', 'is_rh', 'is_ab', 'is_bh', 'is_gh',
            'is_dgw', 'is_egw', 'is_gc', 'is_gw',
            'is_ms', 'is_phw', 'is_apt', 'is_wg',
            ]


def getRentAptFeatures():
    return [
        'rooms', 'has_carport', 'has_elevator', 'has_garage', 'has_cellar', 'has_parking', 'has_closet',
        'has_balcony',
        'has_terrace', 'has_wintergarden', 'is_pellets', 'is_photovoltaik', 'is_floor',
        'is_oven', 'balcony_ratio', 'terrace_ratio', 'is_urban', 'is_egw', 'is_ms', 'is_apt', 'log_living_area',
        'log_estate_size', 'log_balcony_size', 'log_garden_size', 'log_terrace_size', 'log_loggia_size',
        'log_distance_nearest_city', 'log_distance_nearest_lake', 'log_distance_villach', 'log_distance_klagenfurt',
        'loc_14_0', 'loc_14_1', 'loc_14_2', 'loc_14_3', 'loc_14_4', 'loc_14_5', 'loc_14_9', 'loc_14_10',
        'loc_14_11', 'loc_14_12',
        'loc_14_13']


def getBuyAptFeatures():
    return ['rooms', 'has_carport', 'has_elevator', 'has_garage', 'has_cellar', 'has_parking', 'has_closet',
            'has_balcony', 'has_garden', 'has_terrace', 'has_loggia', 'has_wintergarden', 'is_oil', 'is_pellets',
            'is_photovoltaik', 'is_geothermal', 'is_air_heating', 'is_floor', 'is_central', 'is_oven', 'is_infrared',
            'balcony_ratio', 'garden_ratio', 'terrace_ratio', 'is_urban', 'is_dgw', 'is_egw', 'is_gc', 'is_gw', 'is_ms',
            'is_phw', 'is_apt', 'is_wg', 'log_living_area', 'log_estate_size', 'log_balcony_size', 'log_garden_size',
            'log_terrace_size', 'log_loggia_size', 'log_distance_nearest_city', 'log_distance_nearest_lake',
            'log_distance_villach', 'log_distance_klagenfurt', 'loc_14_0', 'loc_14_1', 'loc_14_2', 'loc_14_3',
            'loc_14_4', 'loc_14_5', 'loc_14_9', 'loc_14_11', 'loc_14_12', 'loc_14_13'
            ]


def getRentHouseFeatures():
    return [
        'rooms', 'has_carport', 'has_elevator', 'has_garage', 'has_cellar', 'has_parking', 'has_closet', 'has_balcony',
        'has_terrace', 'has_wintergarden', 'is_pellets', 'is_photovoltaik', 'is_floor', 'is_oven', 'balcony_ratio',
        'terrace_ratio', 'is_urban', 'is_mfh', 'is_efh', 'is_lh', 'is_villa', 'is_dhh', 'is_sbc', 'is_rh', 'is_ab',
        'is_bh', 'is_gh', 'is_egw', 'is_ms', 'is_apt', 'log_living_area', 'log_estate_size', 'log_balcony_size',
        'log_garden_size', 'log_terrace_size', 'log_loggia_size', 'log_distance_nearest_city',
        'log_distance_nearest_lake', 'log_distance_villach', 'log_distance_klagenfurt', 'loc_14_0', 'loc_14_1',
        'loc_14_2', 'loc_14_3', 'loc_14_4', 'loc_14_5', 'loc_14_9', 'loc_14_10', 'loc_14_11', 'loc_14_12', 'loc_14_13'
    ]


def getBuyHouseFeatures():
    return ['rooms', 'has_carport', 'has_elevator', 'has_garage', 'has_cellar', 'has_parking', 'has_closet',
            'has_balcony', 'has_garden', 'has_terrace', 'has_loggia', 'has_wintergarden', 'is_oil', 'is_pellets',
            'is_photovoltaik', 'is_geothermal', 'is_air_heating', 'is_floor', 'is_central', 'is_oven', 'is_infrared',
            'balcony_ratio', 'garden_ratio', 'terrace_ratio', 'is_urban', 'is_mfh', 'is_efh', 'is_lh', 'is_dgw',
            'is_egw', 'is_gc', 'is_gw', 'is_ms', 'is_phw', 'is_apt', 'is_wg', 'log_living_area', 'log_estate_size',
            'log_balcony_size', 'log_garden_size', 'log_terrace_size', 'log_loggia_size', 'log_distance_nearest_city',
            'log_distance_nearest_lake', 'log_distance_villach', 'log_distance_klagenfurt', 'loc_14_0', 'loc_14_1',
            'loc_14_2', 'loc_14_3', 'loc_14_4', 'loc_14_5', 'loc_14_9', 'loc_14_11', 'loc_14_12', 'loc_14_13']
