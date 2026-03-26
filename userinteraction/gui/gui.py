from mlModels.kmeans.locationClustering import addLocationFeature
from userinteraction.gui.guiData import getColumnList, getRentAptFeatures, getBuyAptFeatures, getRentHouseFeatures, getBuyHouseFeatures, setTerminateFlag
from datamanipulation.cleanData import getLogNorm, getRatio, computeDistances, getIsUrban, getLocations
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from imreg import main
from tkinter import ttk

import tkinter as tk
import pandas as pd
import numpy as np
import joblib, threading, logging, subprocess, time

geolocator = Nominatim(user_agent="ImmoScraper")
is_running = False

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def getCoordinates(addr):
    logging.info(f"Getting coordinates for address {addr}")
    location = geolocator.geocode(addr)
    if location:
        logging.info(f"Coordinates found: {location.latitude}, {location.longitude}")
        return location.latitude, location.longitude
    else:
        return None, None

def getFloat(entry, default=0):
    value = entry.get().strip()
    return float(value) if value != "" else default

def featureSelection(df, feature_list):
    if feature_list is None:
        logging.warning("No features has been selected due to property and finance type mismatch")
        return df

    df_features = df.copy()
    df_features = df_features[[col for col in feature_list if col in df_features.columns]]
    for col in feature_list:
        if col not in df_features.columns:
            df_features[col] = 0

    df_features = df_features[feature_list]
    return df_features


def gui():
    root = tk.Tk()
    root.title("ImmoScraper")
    root.config(bg="#E4E2E2")
    root.geometry("1280x665")
    root.update_idletasks()

    geometryX = 0
    geometryY = 0

    root.geometry("+%d+%d"%(geometryX, geometryY))


    style = ttk.Style(root)
    style.theme_use("clam")

    frame = tk.Frame(master=root)
    frame.config(bg="#BCBCBC")
    frame.place(x=26, y=494, width=1230, height=143)

    frame_right = tk.Frame(master=root)
    frame_right.config(bg="#BCBCBC")
    frame_right.place(x=650, y=26, width=600, height=450)

    frame_output = tk.Frame(master=frame_right)
    frame_output.config(bg="#EDECEC")
    frame_output.place(x=26, y=234, width=546, height=198)

    frame_left = tk.Frame(master=root)
    frame_left.config(bg="#BCBCBC")
    frame_left.place(x=26, y=26, width=600, height=450)

    style.configure("scraping.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("scraping.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    do_scraping = tk.BooleanVar()
    scraping = ttk.Checkbutton(master=frame, text="Scraping", style="scraping.TCheckbutton", variable=do_scraping)
    scraping.place(x=26, y=26, width=120, height=30)

    style.configure("clean_data.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("clean_data.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    do_clean_data = tk.BooleanVar()
    clean_data = ttk.Checkbutton(master=frame, text="Clean Data", style="clean_data.TCheckbutton", variable=do_clean_data)
    clean_data.place(x=26, y=78, width=120, height=30)

    style.configure("train_model.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("train_model.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    do_train_model= tk.BooleanVar()
    train_model = ttk.Checkbutton(master=frame, text="Train Model", style="train_model.TCheckbutton", variable=do_train_model)
    train_model.place(x=182, y=26, width=120, height=30)

    style.configure("carport.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("carport.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_carport_var = tk.BooleanVar()
    carport = ttk.Checkbutton(master=frame_left, text="Carport", style="carport.TCheckbutton", variable=has_carport_var)
    carport.place(x=26, y=26, width=120, height=30)

    style.configure("elevator.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("elevator.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_elevator_var = tk.BooleanVar()
    elevator = ttk.Checkbutton(master=frame_left, text="Elevator", style="elevator.TCheckbutton", variable=has_elevator_var)
    elevator.place(x=26, y=52, width=120, height=30)

    style.configure("kitchen.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("kitchen.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_kitchen_var = tk.BooleanVar()
    kitchen = ttk.Checkbutton(master=frame_left, text="Kitchen", style="kitchen.TCheckbutton", variable=has_kitchen_var)
    kitchen.place(x=26, y=78, width=120, height=30)

    style.configure("garage.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("garage.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_garage_var = tk.BooleanVar()
    garage = ttk.Checkbutton(master=frame_left, text="Garage", style="garage.TCheckbutton", variable=has_garage_var)
    garage.place(x=26, y=104, width=120, height=30)

    style.configure("cellar.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("cellar.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_cellar_var = tk.BooleanVar()
    cellar = ttk.Checkbutton(master=frame_left, text="Cellar", style="cellar.TCheckbutton", variable=has_cellar_var)
    cellar.place(x=26, y=130, width=120, height=30)

    style.configure("parking.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("parking.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_parking_var = tk.BooleanVar()
    parking = ttk.Checkbutton(master=frame_left, text="Parking", style="parking.TCheckbutton", variable=has_parking_var)
    parking.place(x=26, y=156, width=120, height=30)

    style.configure("closet.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("closet.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_closet_var = tk.BooleanVar()
    closet = ttk.Checkbutton(master=frame_left, text="Closet", style="closet.TCheckbutton", variable=has_closet_var)
    closet.place(x=26, y=182, width=120, height=30)

    style.configure("wintergarden.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("wintergarden.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_wintergarden_var = tk.BooleanVar()
    wintergarden = ttk.Checkbutton(master=frame_left, text="Wintergarden", style="wintergarden.TCheckbutton", variable=has_wintergarden_var)
    wintergarden.place(x=21, y=399, width=120, height=30)

    style.configure("loggia.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("loggia.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_loggia_var = tk.BooleanVar()
    loggia = ttk.Checkbutton(master=frame_left, text="Loggia", style="loggia.TCheckbutton", variable=has_loggia_var)
    loggia.place(x=21, y=357, width=120, height=30)

    style.configure("terrace.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("terrace.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_terrace_var = tk.BooleanVar()
    terrace = ttk.Checkbutton(master=frame_left, text="Terrace", style="terrace.TCheckbutton", variable=has_terrace_var)
    terrace.place(x=21, y=315, width=120, height=30)

    style.configure("garden.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("garden.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_garden_var = tk.BooleanVar()
    garden = ttk.Checkbutton(master=frame_left, text="Garden", style="garden.TCheckbutton", variable=has_garden_var)
    garden.place(x=21, y=273, width=120, height=30)

    style.configure("balcony.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("balcony.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    has_balcony_var = tk.BooleanVar()
    balcony = ttk.Checkbutton(master=frame_left, text="Balcony", style="balcony.TCheckbutton", variable=has_balcony_var)
    balcony.place(x=21, y=231, width=120, height=30)

    # Rent & Buy
    rent_var = tk.IntVar()
    style.configure("rent.TRadiobutton", background="#E4E2E2", foreground="#000")
    style.map("rent.TRadiobutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    rent_0 = ttk.Radiobutton(master=frame_right, variable=rent_var, text="Rent", value=0, style="rent.TRadiobutton")
    rent_0.place(x=495, y=26, width=80, height=24)

    rent_1 = ttk.Radiobutton(master=frame_right, variable=rent_var, text="Buy", value=1, style="rent.TRadiobutton")
    rent_1.place(x=495, y=50, width=80, height=24)

    # Apartment & House
    apt_var = tk.IntVar()
    style.configure("apt.TRadiobutton", background="#E4E2E2", foreground="#000")
    style.map("apt.TRadiobutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    apt_0 = ttk.Radiobutton(master=frame_right, variable=apt_var, text="Apartment", value=0, style="apt.TRadiobutton")
    apt_0.place(x=475, y=84, width=110, height=24)

    apt_1 = ttk.Radiobutton(master=frame_right, variable=apt_var, text="House", value=1, style="apt.TRadiobutton")
    apt_1.place(x=475, y=108, width=110, height=24)


    # Living Area
    tk.Label(frame_right, text="Living Area:", bg="#BCBCBC").place(x=26, y=6)
    entry_living_area = ttk.Entry(master=frame_right, style="entry_living_area.TEntry")
    entry_living_area.place(x=26, y=26, width=155, height=25)

    # Rooms
    tk.Label(frame_right, text="Rooms:", bg="#BCBCBC").place(x=26, y=58)
    entry_rooms = ttk.Entry(master=frame_right, style="entry_rooms.TEntry")
    entry_rooms.place(x=26, y=78, width=155, height=25)

    # Postcode
    tk.Label(frame_right, text="Postcode:", bg="#BCBCBC").place(x=26, y=110)
    entry_postcode = ttk.Entry(master=frame_right, style="entry_postcode.TEntry")
    entry_postcode.place(x=26, y=130, width=155, height=25)

    # Address
    tk.Label(frame_right, text="Address:", bg="#BCBCBC").place(x=26, y=162)
    entry_address = ttk.Entry(master=frame_right, style="entry_address.TEntry")
    entry_address.place(x=26, y=182, width=313, height=25)

    # Balcony Size:
    tk.Label(frame_left, text="Balcony Size:", bg="#BCBCBC").place(x=200, y=231)
    entry_balcony_size = ttk.Entry(master=frame_left, style="entry_balcony_size.TEntry")
    entry_balcony_size.place(x=335, y=231, width=130, height=25)

    # Garden Size:
    tk.Label(frame_left, text="Garden Size:", bg="#BCBCBC").place(x=200, y=273)
    entry_garden_size = ttk.Entry(master=frame_left, style="entry_garden_size.TEntry")
    entry_garden_size.place(x=336, y=273, width=130, height=25)

    # Terrace Size:
    tk.Label(frame_left, text="Terrace Size:", bg="#BCBCBC").place(x=200, y=315)
    entry_terrace_size = ttk.Entry(master=frame_left, style="entry_terrace_size.TEntry")
    entry_terrace_size.place(x=336, y=315, width=130, height=25)

    # Loggia Size:
    tk.Label(frame_left, text="Loggia Size:", bg="#BCBCBC").place(x=200, y=357)
    entry_loggia_size = ttk.Entry(master=frame_left, style="entry_loggia_size.TEntry")
    entry_loggia_size.place(x=336, y=357, width=130, height=25)

    # Wintergarden Size:
    tk.Label(frame_left, text="Wintergarden Size:", bg="#BCBCBC").place(x=200, y=399)
    entry_wintergarden_size = ttk.Entry(master=frame_left, style="entry_wintergarden_size.TEntry")
    entry_wintergarden_size.place(x=336, y=399, width=130, height=25)

    # --- Heating Source dropdown ---
    tk.Label(frame_left, text="Heating Source:", bg="#BCBCBC").place(x=336, y=26)
    heating_source_var = tk.StringVar()
    heating_source = ttk.Combobox(
        frame_left,
        textvariable=heating_source_var,
        state="readonly",
        values=[
            "Select", "Oil", "Bio", "Electric", "Pellets",
            "Photovoltaik", "Geothermal", "Air source heating pump"
        ]
    )
    heating_source.place(x=336, y=51, width=155, height=25)
    heating_source.current(0)
    selected_heating = heating_source_var.get()
    is_oil_var = 1 if selected_heating == "Oil" else 0
    is_bio_var = 1 if selected_heating == "Bio" else 0
    is_electro_var = 1 if selected_heating == "Electric" else 0
    is_pellets_var = 1 if selected_heating == "Pellets" else 0
    is_photovoltaik_var = 1 if selected_heating == "Photovoltaik" else 0
    is_geothermal_var = 1 if selected_heating == "Geothermal" else 0
    is_air_heating_var = 1 if selected_heating == "Air source heating pump" else 0

    # Heating Type dropdown
    tk.Label(frame_left, text="Heating Type:", bg="#BCBCBC").place(x=336, y=85)
    heating_type_var = tk.StringVar()
    heating_type = ttk.Combobox(frame_left, textvariable=heating_type_var, state="readonly",
                                values=["Select", "Floor", "Central", "Ceiling", "Oven", "Infrared"])
    heating_type.place(x=336, y=110, width=155, height=25)
    heating_type.current(0)
    selected_heating_type = heating_type_var.get()
    is_floor_var = 1 if selected_heating_type == "Floor" else 0
    is_central_var = 1 if selected_heating_type == "Central" else 0
    is_ceiling_var = 1 if selected_heating_type == "Ceiling" else 0
    is_oven_var = 1 if selected_heating_type == "Oven" else 0
    is_infrared_var = 1 if selected_heating_type == "Infrared" else 0


    # --- HWB / fgEE Block ---
    # HWB + fgEE
    tk.Label(frame_right, text="HWB:", bg="#BCBCBC").place(x=200, y=6)
    entry_hwb = ttk.Entry(frame_right)
    entry_hwb.place(x=200, y=26, width=120, height=25)


    tk.Label(frame_right, text="fgEE:", bg="#BCBCBC").place(x=340, y=6)
    entry_fgee = ttk.Entry(frame_right)
    entry_fgee.place(x=340, y=26, width=120, height=25)


    # HWB Class + fgEE Class
    tk.Label(frame_right, text="HWB Class:", bg="#BCBCBC").place(x=200, y=58)
    entry_hwb_class = ttk.Entry(frame_right)
    entry_hwb_class.place(x=200, y=78, width=120, height=25)

    tk.Label(frame_right, text="fgEE Class:", bg="#BCBCBC").place(x=340, y=58)
    entry_fgee_class = ttk.Entry(frame_right)
    entry_fgee_class.place(x=340, y=78, width=120, height=25)

    # --- Property Type Dropdown (dynamic) ---
    property_type_var = tk.StringVar()
    property_type_label = tk.Label(frame_right, text="Property Type:", bg="#BCBCBC")
    property_type_dropdown = ttk.Combobox(frame_right, textvariable=property_type_var, state="readonly")
    apartment_types = [
        "Select",
        "Roof Apartment", "Ground Floor Apartment", "Garconniere",
        "Coop Apartment", "Maisonette", "Penthouse", "Apartment", "Room"
    ]
    house_types = [
        "Select",
        "Multifamily House", "Single Family House", "Landhaus",
        "Villa", "Double House", "Castle/Chalet",
        "Row House", "Mountain Cabin", "Farmer House", "Cooperative House"
    ]
    def update_property_dropdown():
        val = apt_var.get()
        if val == 0:
            property_type_dropdown["values"] = apartment_types
            property_type_dropdown.current(0)
            property_type_label.place(x=200, y=110)
            property_type_dropdown.place(x=200, y=130, width=200, height=25)
        elif val == 1:
            property_type_dropdown["values"] = house_types
            property_type_dropdown.current(0)
            property_type_label.place(x=200, y=110)
            property_type_dropdown.place(x=200, y=130, width=200, height=25)
        else:
            property_type_label.place_forget()
            property_type_dropdown.place_forget()
    apt_var.trace_add("write", lambda *args: update_property_dropdown())
    update_property_dropdown()
    selected_property = property_type_var.get()
    is_dgw_var = 1 if selected_property == "Roof Apartment" else 0
    is_egw_var = 1 if selected_property == "Ground Floor Apartment" else 0
    is_gc_var = 1 if selected_property == "Garconniere" else 0
    is_gw_var = 1 if selected_property == "Coop Apartment" else 0
    is_ms_var = 1 if selected_property == "Maisonette" else 0
    is_phw_var = 1 if selected_property == "Penthouse" else 0
    is_apt_var = 1 if selected_property == "Apartment" else 0
    is_wg_var = 1 if selected_property == "Room" else 0
    is_mfh_var = 1 if selected_property == "Multifamily House" else 0
    is_efh_var = 1 if selected_property == "Single Family House" else 0
    is_lh_var = 1 if selected_property == "Landhaus" else 0
    is_villa_var = 1 if selected_property == "Villa" else 0
    is_dhh_var = 1 if selected_property == "Double House" else 0
    is_sbc_var = 1 if selected_property == "Castle/Chalet" else 0
    is_rh_var = 1 if selected_property == "Row House" else 0
    is_ab_var = 1 if selected_property == "Mountain Cabin" else 0
    is_bh_var = 1 if selected_property == "Farmer House" else 0
    is_gh_var = 1 if selected_property == "Cooperative House" else 0

    # Output
    output_var = tk.StringVar()
    output_label = tk.Label(
        frame_output,
        textvariable=output_var,
        bg="#EDECEC",
        font=("Arial", 20, "bold"),
        fg="#2E7D32"
    )
    output_label.place(x=20, y=20)


    def _backendRun():
        subprocess.run(["sudo", "systemctl", "start", "postgresql"])
        time.sleep(3)
        if do_scraping.get():
            do_clean_data.set(True)
        main(SOURCE_1=True, SCRAPE_SOURCE_1=do_scraping.get(), CLEAN_DATA=do_clean_data.get(), MODELS=do_train_model.get()) # TODO create entries for ROWS and PAGES
        subprocess.run(["sudo", "systemctl", "stop", "postgresql"])


    def backendRun():
        global is_running
        if is_running:
            return
        is_running = True

        def run():
            global is_running
            _backendRun()
            setTerminateFlag(False)
            is_running = False
        threading.Thread(target=run).start()

    def chooseModel():
        base_path = "mlModels/regression/data/"

        if apt_var.get() == 1 and rent_var.get() == 0:
            model = "rent_house_model.pkl"
        elif apt_var.get() == 1 and rent_var.get() == 1:
            model = "buy_house_model.pkl"
        elif apt_var.get() == 0 and rent_var.get() == 0:
            model = "rent_apt_model.pkl"
        elif apt_var.get() == 0 and rent_var.get() == 1:
            model = "buy_apt_model.pkl"
        else:
            logging.warning("No model could be selected")
            raise ValueError("No model could be selected")

        scaler = joblib.load("mlModels/kmeans/data/scaler.pkl")
        kmeans = joblib.load("mlModels/kmeans/data/kmeans.pkl")
        log_model = base_path + model
        logging.info(f"Selected model: {log_model}")

        data = joblib.load(log_model)
        return data, scaler, kmeans


    def makePrediction():
        try:
            input_id = -1
            living_area = getFloat(entry_living_area)
            estate_size = living_area
            rooms = getFloat(entry_rooms)
            lat, lon = getCoordinates(entry_address.get() + "," + entry_postcode.get())
            postcode = getFloat(entry_postcode)
            has_carport = has_carport_var.get()
            has_elevator = has_elevator_var.get()
            has_kitchen = has_kitchen_var.get()
            has_garage = has_garage_var.get()
            has_cellar = has_cellar_var.get()
            has_parking = has_parking_var.get()
            has_closet = has_closet_var.get()
            has_balcony = has_balcony_var.get()
            balcony_size = getFloat(entry_balcony_size)
            has_garden = has_garden_var.get()
            garden_size = getFloat(entry_garden_size)
            has_terrace = has_terrace_var.get()
            terrace_size = getFloat(entry_terrace_size)
            has_loggia = has_loggia_var.get()
            loggia_size = getFloat(entry_loggia_size)
            has_wintergarden = has_wintergarden_var.get()
            wintergarden_size = getFloat(entry_wintergarden_size)
            is_oil = is_oil_var
            is_bio = is_bio_var
            is_electro = is_electro_var
            is_pellets = is_pellets_var
            is_photovoltaik = is_photovoltaik_var
            is_geothermal = is_geothermal_var
            is_air_heating = is_air_heating_var
            is_floor = is_floor_var
            is_central = is_central_var
            is_ceiling = is_ceiling_var
            is_oven = is_oven_var
            is_infrared = is_infrared_var
            hwb = getFloat(entry_hwb)
            hwb_class = entry_hwb_class.get()
            fgee = getFloat(entry_fgee)
            fgee_class = entry_fgee_class.get()
            is_mfh = is_mfh_var
            is_efh = is_efh_var
            is_lh = is_lh_var
            is_villa = is_villa_var
            is_dhh = is_dhh_var
            is_sbc = is_sbc_var
            is_rh = is_rh_var
            is_ab = is_ab_var
            is_bh = is_bh_var
            is_gh = is_gh_var
            is_dgw = is_dgw_var
            is_egw = is_egw_var
            is_gc = is_gc_var
            is_gw = is_gw_var
            is_ms = is_ms_var
            is_phw = is_phw_var
            is_apt = is_apt_var
            is_wg = is_wg_var

            features = [[input_id, living_area, estate_size, rooms, lat, lon, postcode, has_carport, has_elevator, has_kitchen, has_garage,
                         has_cellar, has_parking, has_closet,
                         has_balcony, balcony_size, has_garden, garden_size, has_terrace, terrace_size, has_loggia,
                         loggia_size, has_wintergarden, wintergarden_size, is_oil, is_bio, is_electro, is_pellets,
                         is_photovoltaik, is_geothermal, is_air_heating,
                         is_floor, is_central, is_ceiling, is_oven, is_infrared, hwb, hwb_class, fgee, fgee_class, is_mfh,
                         is_efh, is_lh, is_villa, is_dhh, is_sbc, is_rh, is_ab, is_bh, is_gh,
                         is_dgw, is_egw, is_gc, is_gw, is_ms, is_phw, is_apt, is_wg,
                         ]]

            logging.info(f"Prediction called with parameters: {features}")

            features = pd.DataFrame(features, columns=getColumnList())

            features = getRatio(features, "balcony_size", "living_area", "balcony_ratio")
            features = getRatio(features, "terrace_size", "living_area", "terrace_ratio")
            features = getLogNorm(features, "living_area")
            features = getLogNorm(features, "estate_size")
            features = getLogNorm(features, "balcony_size")
            features = getLogNorm(features, "garden_size")
            features = getLogNorm(features, "terrace_size")
            features = getLogNorm(features, "loggia_size")


            # TODO cities, lakes = getLocations()
            # TODO features = computeDistances(features, cities, lakes)
            # TODO features = getIsUrban(features)

            model, scaler, kmeans = chooseModel()
            df_cluster = pd.DataFrame([[input_id, lat, lon]], columns=["id", "lat", "lon"])
            df_cluster_features = addLocationFeature(df_cluster, scaler, kmeans, n_clusters=14)

            features = pd.concat([features, df_cluster_features], axis=1)
            features = features.loc[:, ~features.columns.duplicated()]

            df_features = featureSelection(features,
                                           getRentAptFeatures() if (rent_var.get() == 0 and apt_var.get() == 0)
                                           else getBuyAptFeatures() if (rent_var.get() == 1 and apt_var.get() == 0)
                                           else getRentHouseFeatures() if (rent_var.get() == 0 and apt_var.get() == 1)
                                           else getBuyHouseFeatures() if (rent_var.get() == 1 and apt_var.get() == 1)
                                           else None
                                           )

            prediction = model.predict(df_features)[0]

            if prediction:
                prediction = np.exp(prediction) - 1

            output_var.set(f"{prediction:.2f} €" if prediction is not None else "No model")
            logging.info(f"-------Finished prediction with prediction {prediction}-------")

        except ValueError:
            logging.exception("Value Error")
            output_var.set("Invalid input")

    # Predict Button
    style.configure("button1.TButton", background="#E4E2E2", foreground="#000")
    style.map("button1.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    button1 = ttk.Button(master=frame_right, text="Predict", style="button1.TButton", command=makePrediction)
    button1.place(x=495, y=176, width=80, height=40)

    # Start Backend Button
    style.configure("button.TButton", background="#E4E2E2", foreground="#000")
    style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    button = ttk.Button(master=frame, text="Start Backend", style="button.TButton", command=backendRun)
    button.place(x=1101, y=78, height=40, width=120)

    # Terminate Button
    style.configure("button.TButton", background="#E4E2E2", foreground="#000")
    style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
    terminate_button = ttk.Button(master=frame, text="Stop Backend", style="button.TButton", command=lambda: setTerminateFlag(True))
    terminate_button.place(x=1101, y=28, height=40, width=120)

    root.mainloop()





