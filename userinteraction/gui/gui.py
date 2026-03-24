from mlModels.kmeans.locationClustering import addLocationFeature
from datamanipulation.cleanData import getLogNorm, getRatio, computeDistances, getIsUrban
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from imreg import main

import joblib, threading
import tkinter as tk
import pandas as pd

geolocator = Nominatim(user_agent="ImmoScraper")

def backendRun():
    threading.Thread(target=_backendRun).start()


def _backendRun():
    if do_scraping.get():
        do_cleaning.set(True)
    main(SOURCE_1=source1.get(), SCRAPE_SOURCE_1=do_scraping.get(), MODELS=do_training.get())


def getCoordinates(a):
    location = geolocator.geocode(a)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def chooseModel(is_house, is_apartment):
    base_path = "mlModels/regression/data/"
    model = ""
    if is_house and rent_checkbox.get():
        model = "rent_house_model.pkl"
    elif is_house and buy_checkbox.get():
        model = "buy_house_model.pkl"
    elif is_apartment and rent_checkbox.get():
        model = "rent_apt_model.pkl"
    elif is_apartment and buy_checkbox.get():
        model = "buy_apt_model.pkl"
    else:
        raise ValueError("No model could be selected")

    scaler = joblib.load("mlModels/kmeans/data/scaler.pkl")
    kmeans = joblib.load("mlModels/kmeans/data/kmeans.pkl")
    log_model = base_path + model

    data = joblib.load(log_model)
    return data, scaler, kmeans

def makePrediction():
    is_house = False
    is_apartment = False

    if not (rent_checkbox.get() ^ buy_checkbox.get()):
        output_var.set("Exactly one of Rent or Buy must be selected")
        return

    house_types = [
        is_mfh.get(), is_efh.get(), is_lh.get(), is_villa.get(),
        is_dhh.get(), is_sbc.get(), is_rh.get(), is_ab.get(),
        is_bh.get(), is_gh.get()
    ]

    apt_types = [
        is_dgw.get(), is_egw.get(), is_gc.get(), is_gw.get(),
        is_ms.get(), is_phw.get(), is_apt.get(), is_wg.get()
    ]

    if sum(house_types + apt_types) != 1:
        output_var.set("Exactly one house/apartment type must be selected")
        return

    if is_msg.get() ^ is_efh.get() ^ is_lh.get() ^ is_villa.get() ^ is_dhh.get() ^ is_sbc.get() ^ is_rh.get() ^ is_ab.get() ^ is_bh.get() ^ is_gh.get():
        is_house = True
        is_apartment = False

    elif is_dgw.get() ^ is_egw.get() ^ is_gc.get() ^ is_gw.get() ^ is_ms.get() ^ is_phw.get() ^ is_apt.get() ^ is_wg.get():
        is_house = False
        is_apartment = True

    try:
        id = -1
        area = float(living_area.get())
        rooms = int(entry_rooms.get())
        lat, lon = getCoordinates(address.get())
        postcode = int(postcode.get())
        has_carport = has_carport_var.get()
        has_elevator = has_elevator_var.get()
        has_kitchen = has_kitchen_var.get()
        has_garage = has_garage_var.get()
        has_cellar = has_cellar_var.get()
        has_parking = has_parking_var.get()
        has_closet = has_closet_var.get()
        has_balcony = has_balcony_var.get()
        balcony_size = float(entry_balcony_size.get())
        has_garden = has_garden_var.get()
        garden_size = float(entry_garden_size.get())
        has_terrace = has_terrace_var.get()
        terrace_size = float(entry_terrace_size.get())
        has_loggia = has_loggia_var.get()
        loggia_size = float(entry_loggia_size.get())
        has_wintergarden = has_wintergarden_var.get()
        wintergarden_size = float(entry_wintergarden_size.get())
        is_oil = is_oil_var.get()
        is_bio = is_bio_var.get()
        is_electro = is_electro_var.get()
        is_pellets = is_pellets_var.get()
        is_photovoltaik = is_photovoltaik_var.get()
        is_geothermal = is_geothermal_var.get()
        is_air_heating = is_air_heating_var.get()
        is_floor = is_floor_var.get()
        is_central = is_central_var.get()
        is_ceiling = is_ceiling_var.get()
        is_oven = is_oven_var.get()
        is_infrared = is_infrared_var.get()
        hwb = float(entry_hwb.get())
        hwb_class = entry_hwb_class.get()
        fgee = float(entry_fgee.get())
        fgee_class = entry_fgee_class.get()
        is_mfh = is_mfh_var.get()
        is_efh = is_efh_var.get()
        is_lh = is_lh_var.get()
        is_villa = is_villa_var.get()
        is_dhh = is_dhh_var.get()
        is_sbc = is_sbc_var.get()
        is_rh = is_rh_var.get()
        is_ab = is_ab_var.get()
        is_bh = is_bh_var.get()
        is_gh = is_gh_var.get()
        is_dgw = is_dgw_var.get()
        is_egw = is_egw_var.get()
        is_gc = is_gc_var.get()
        is_gw = is_gw_var.get()
        is_ms = is_ms_var.get()
        is_phw = is_phw_var.get()
        is_apt = is_apt_var.get()
        is_wg = is_wg_var.get()

        features = [[id, area, rooms, lat, lon, postcode, has_carport, has_elevator, has_kitchen, has_garage,
                     has_cellar, has_parking, has_closet,
                     has_balcony, balcony_size, has_garden, garden_size, has_terrace, terrace_size, has_loggia,
                     loggia_size, has_wintergarden, wintergarden_size, is_oil, is_bio, is_electro, is_pellets,
                     is_photovoltaik, is_geothermal, is_air_heating,
                     is_floor, is_central, is_ceiling, is_oven, is_infrared, hwb, hwb_class, fgee, fgee_class, is_mfh,
                     is_efh, is_lh, is_villa, is_dhh, is_sbc, is_rh, is_ab, is_bh, is_gh,
                     is_dgw, is_egw, is_gc, is_gw, is_ms, is_phw, is_apt, is_wg,
                    ]]

        features = pd.DataFrame(features,
                                columns=['id', 'area', 'rooms', 'lat', 'lon', 'postcode', 'has_carport',
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
                                         ])

        features = getRatio(features, "balcony_size", "living_area", "balcony_ratio")
        features = getRatio(features, "terrace_size", "living_area", "terrace_ratio")
        features = getLogNorm(features, "living_area")
        features = getLogNorm(features, "estate_size")
        features = getLogNorm(features, "balcony_size")
        features = getLogNorm(features, "garden_size")
        features = getLogNorm(features, "terrace_size")
        features = getLogNorm(features, "loggia_size")

        cities, lakes = getLocations()
        features = computeDistances(features, cities, lakes)
        features = getIsUrban(features)

        featureset_rent = features.copy()
        featureset_buy = features.copy()

        rent_features = [
            'rooms', 'has_carport', 'has_elevator', 'has_garage', 'has_cellar', 'has_parking', 'has_closet',
            'has_balcony',
            'has_terrace', 'has_wintergarden', 'is_pellets', 'is_photovoltaik', 'is_floor',
            'is_oven', 'balcony_ratio', 'terrace_ratio', 'is_urban', 'is_mfh', 'is_efh', 'is_lh', 'is_villa', 'is_dhh',
            'is_sbc', 'is_rh',
            'is_ab', 'is_bh', 'is_gh', 'is_egw', 'is_ms', 'is_apt', 'log_living_area',
            'log_estate_size', 'log_balcony_size', 'log_garden_size', 'log_terrace_size', 'log_loggia_size',
            'log_distance_nearest_city', 'log_distance_nearest_lake', 'log_distance_villach', 'log_distance_klagenfurt',
            'loc_14_0', 'loc_14_1', 'loc_14_2', 'loc_14_3', 'loc_14_4', 'loc_14_5', 'loc_14_9', 'loc_14_10',
            'loc_14_11', 'loc_14_12',
            'loc_14_13']

        buy_features = ['rooms', 'has_carport', 'has_elevator', 'has_garage', 'has_cellar',
                        'has_parking', 'has_closet', 'has_balcony', 'has_garden', 'has_terrace',
                        'has_loggia', 'has_wintergarden', 'is_oil', 'is_pellets',
                        'is_photovoltaik', 'is_geothermal', 'is_air_heating', 'is_floor',
                        'is_central', 'is_oven', 'is_infrared', 'balcony_ratio', 'garden_ratio',
                        'terrace_ratio', 'is_urban', 'is_mfh', 'is_efh', 'is_lh', 'is_dgw',
                        'is_egw', 'is_gc', 'is_gw', 'is_ms', 'is_phw', 'is_apt', 'is_wg',
                        'log_living_area', 'log_estate_size', 'log_balcony_size',
                        'log_garden_size', 'log_terrace_size', 'log_loggia_size',
                        'log_distance_nearest_city', 'log_distance_nearest_lake',
                        'log_distance_villach', 'log_distance_klagenfurt', 'loc_14_0',
                        'loc_14_1', 'loc_14_2', 'loc_14_3', 'loc_14_4', 'loc_14_5', 'loc_14_9',
                        'loc_14_11', 'loc_14_12', 'loc_14_13']

        model, scaler, kmeans = chooseModel(is_house, is_apartment)
        df_cluster = pd.DataFrame([[id, lat, lon]], columns=["id", "lat", "lon"])
        df_buy_cluster_features = addLocationFeature(df_cluster, scaler, kmeans, n_clusters=14)
        df_rent_cluster_features = addLocationFeature(df_cluster, scaler, kmeans, n_clusters=14)

        featureset_buy = pd.concat([featureset_buy, df_buy_cluster_features], axis=1)
        featureset_rent = pd.concat([featureset_rent, df_rent_cluster_features], axis=1)

        df_rent_features = featureset_rent.reindex(columns=rent_features, fill_value=0)
        df_buy_features = featureset_buy.reindex(columns=buy_features, fill_value=0)

        prediction = None

        if rent_checkbox.get():
            prediction = model.predict(df_rent_features)[0]
        elif buy_checkbox.get():
            prediction = model.predict(df_buy_features)[0]

        output_var.set(f"{prediction:.2f} €" if prediction is not None else "No model")

    except ValueError:
        output_var.set("Invalid input")


def create_checkbox(parent, text):
    var = tk.BooleanVar()
    tk.Checkbutton(parent, text=text, variable=var).pack(anchor="w")
    return var


def create_entry(parent, text):
    tk.Label(parent, text=text).pack(anchor="w")
    entry = tk.Entry(parent)
    entry.pack(anchor="w")
    return entry

def create_button(parent, text, command, side):
    tk.Button(parent, text=text, command=command).pack(side=side, padx=10)

root = tk.Tk()
root.title("ImmoScraper")
root.geometry("1280x720")
root.resizable(False, False)

left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
left_left_frame = tk.Frame(left_frame)
left_left_frame.pack(side="left", pady=20)
left_right_frame = tk.Frame(left_frame)
left_right_frame.pack(side="right", pady=20)

right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
right_left_frame = tk.Frame(right_frame)
right_left_frame.pack(side="left", pady=20)
right_right_frame = tk.Frame(right_frame)
right_right_frame.pack(side="right", pady=20)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="both", expand=True, pady=20)

# Frontend
rent_checkbox = create_checkbox(right_left_frame, "Rent")
buy_checkbox = create_checkbox(right_left_frame, "Buy")
# ------------------------
# Basic Data
# ------------------------

living_area = create_entry(right_right_frame, "Living Area")
entry_rooms = create_entry(right_right_frame, "Rooms")
address = create_entry(right_right_frame, "Address")
postcode = create_entry(right_right_frame, "Postcode")

# ------------------------
# Basic Features
# ------------------------
has_carport = create_checkbox(left_left_frame, "Carport")
has_elevator = create_checkbox(left_left_frame, "Elevator")
has_kitchen = create_checkbox(left_left_frame, "Kitchen")
has_garage = create_checkbox(left_left_frame, "Garage")
has_cellar = create_checkbox(left_left_frame, "Cellar")
has_parking = create_checkbox(left_left_frame, "Parking")
has_closet = create_checkbox(left_left_frame, "Closet")

has_balcony = create_checkbox(left_left_frame, "Balcony")
balcony_size = create_entry(right_right_frame, "Balcony Size")

has_garden = create_checkbox(left_left_frame, "Garden")
garden_size = create_entry(right_right_frame, "Garden Size")

has_terrace = create_checkbox(left_left_frame, "Terrace")
terrace_size = create_entry(right_right_frame, "Terrace Size")

has_loggia = create_checkbox(left_left_frame, "Loggia")
loggia_size = create_entry(right_right_frame, "Loggia Size")

has_wintergarden = create_checkbox(left_left_frame, "Wintergarden")
wintergarden_size = create_entry(right_right_frame, "Wintergarden Size")

# ------------------------
# Heating Source
# ------------------------

is_oil = create_checkbox(left_left_frame, "Oil Heating")
is_bio = create_checkbox(left_left_frame, "Bio Heating")
is_electro = create_checkbox(left_left_frame, "Electro Heating")
is_pellets = create_checkbox(left_left_frame, "Pellets Heating")
is_photovoltaik = create_checkbox(left_left_frame, "Photovoltaik")
is_geothermal = create_checkbox(left_left_frame, "Geothermal")
is_air_heating = create_checkbox(left_left_frame, "Air Heating")

# ------------------------
# Heating Type
# ------------------------

is_floor = create_checkbox(left_left_frame, "Floor Heating")
is_central = create_checkbox(left_left_frame, "Central Heating")
is_ceiling = create_checkbox(left_left_frame, "Ceiling Heating")
is_oven = create_checkbox(left_left_frame, "Oven Heating")
is_infrared = create_checkbox(left_left_frame, "Infrared Heating")

# ------------------------
# Houses
# ------------------------

is_mfh = create_checkbox(left_right_frame, "Multifamily House")
is_efh = create_checkbox(left_right_frame, "Single Family House")
is_lh = create_checkbox(left_right_frame, "Landhaus")
is_villa = create_checkbox(left_right_frame, "Villa")
is_dhh = create_checkbox(left_right_frame, "Double House")
is_sbc = create_checkbox(left_right_frame, "Castle/Chalet")
is_rh = create_checkbox(left_right_frame, "Row House")
is_ab = create_checkbox(left_right_frame, "Mountain Cabin")
is_bh = create_checkbox(left_right_frame, "Farmer House")
is_gh = create_checkbox(left_right_frame, "Cooperative House")

# ------------------------
# Apartments
# ------------------------

is_dgw = create_checkbox(left_right_frame, "Roof Apartment")
is_egw = create_checkbox(left_right_frame, "Ground Floor Apartment")
is_gc = create_checkbox(left_right_frame, "Garconniere")
is_gw = create_checkbox(left_right_frame, "Coop Apartment")
is_ms = create_checkbox(left_right_frame, "Maisonette")
is_phw = create_checkbox(left_right_frame, "Penthouse")
is_apt = create_checkbox(left_right_frame, "Apartment")
is_wg = create_checkbox(left_right_frame, "WG / Room")

# ------------------------
# Energy Values
# ------------------------

hwb = create_entry(right_right_frame, "HWB")
hwb_class = create_entry(right_right_frame, "HWB Class")
fgee = create_entry(right_right_frame, "fgEE")
fgee_class = create_entry(right_right_frame, "fgEE Class")

# ------------------------
# Example: Collect Values
# ------------------------



# Backend
# Checkboxes for backend configuration

do_scraping = create_checkbox(bottom_frame, "Scrape")
do_cleaning = create_checkbox(bottom_frame, "Clean Data")
do_training = create_checkbox(bottom_frame, "Model Training")
source1 = create_checkbox(bottom_frame, "Source 1")

create_button(bottom_frame, "Predict", makePrediction, side="left")
create_button(bottom_frame, "Start Backend", backendRun, side="right")


output_var = tk.StringVar()
output_label = tk.Label(bottom_frame, textvariable=output_var, font=("Arial", 14))
output_label.pack(side="bottom", padx=20)

root.mainloop()
