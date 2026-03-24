from mlModels.kmeans.locationClustering import addLocationFeature
from datamanipulation.cleanData import getLogNorm, getRatio, computeDistances, getIsUrban
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from imreg import main
from tkinter import ttk

import joblib, threading
import tkinter as tk
import pandas as pd

geolocator = Nominatim(user_agent="ImmoScraper")


def gui():
    main = tk.Tk()
    main.title("ImmoScraper")
    main.config(bg="#E4E2E2")
    main.geometry("1280x665")
    main.update_idletasks()

    geometryX = 0
    geometryY = 0

    main.geometry("+%d+%d"%(geometryX, geometryY))


    style = ttk.Style(main)
    style.theme_use("clam")

    menu = tk.Menu(main)

    frame = tk.Frame(master=main)
    frame.config(bg="#BCBCBC")
    frame.place(x=26, y=494, width=1230, height=143)

    style.configure("scraping.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("scraping.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    scraping = ttk.Checkbutton(master=frame, text="Scraping", style="scraping.TCheckbutton")


    scraping.place(x=26, y=26, width=120, height=30)

    style.configure("clean_data.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("clean_data.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    clean_data = ttk.Checkbutton(master=frame, text="Clean Data", style="clean_data.TCheckbutton")


    clean_data.place(x=26, y=78, width=120, height=30)

    style.configure("train_model.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("train_model.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    train_model = ttk.Checkbutton(master=frame, text="Train Model", style="train_model.TCheckbutton")


    train_model.place(x=182, y=26, width=120, height=30)

    style.configure("button.TButton", background="#E4E2E2", foreground="#000")
    style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    button = ttk.Button(master=frame, text="Start Backend", style="button.TButton", command=backendRun)
    button.place(x=1101, y=78, height=40)

    frame_left = tk.Frame(master=main)
    frame_left.config(bg="#BCBCBC")
    frame_left.place(x=26, y=26, width=600, height=450)

    style.configure("carport.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("carport.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    carport = ttk.Checkbutton(master=frame_left, text="Carport", style="carport.TCheckbutton")


    carport.place(x=26, y=26, width=120, height=30)

    style.configure("elevator.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("elevator.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    elevator = ttk.Checkbutton(master=frame_left, text="Elevator", style="elevator.TCheckbutton")


    elevator.place(x=26, y=52, width=120, height=30)

    style.configure("kitchen.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("kitchen.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    kitchen = ttk.Checkbutton(master=frame_left, text="Kitchen", style="kitchen.TCheckbutton")


    kitchen.place(x=26, y=78, width=120, height=30)

    style.configure("garage.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("garage.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    garage = ttk.Checkbutton(master=frame_left, text="Garage", style="garage.TCheckbutton")


    garage.place(x=26, y=104, width=120, height=30)

    style.configure("cellar.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("cellar.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    cellar = ttk.Checkbutton(master=frame_left, text="Cellar", style="cellar.TCheckbutton")


    cellar.place(x=26, y=130, width=120, height=30)

    style.configure("parking.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("parking.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    parking = ttk.Checkbutton(master=frame_left, text="Parking", style="parking.TCheckbutton")


    parking.place(x=26, y=156, width=120, height=30)

    style.configure("closet.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("closet.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    closet = ttk.Checkbutton(master=frame_left, text="Closet", style="closet.TCheckbutton")


    closet.place(x=26, y=182, width=120, height=30)

    style.configure("wintergarden.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("wintergarden.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    wintergarden = ttk.Checkbutton(master=frame_left, text="Wintergarden", style="wintergarden.TCheckbutton")


    wintergarden.place(x=21, y=399, width=120, height=30)

    style.configure("loggia.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("loggia.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    loggia = ttk.Checkbutton(master=frame_left, text="Loggia", style="loggia.TCheckbutton")


    loggia.place(x=21, y=357, width=120, height=30)

    style.configure("terrace.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("terrace.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    terrace = ttk.Checkbutton(master=frame_left, text="Terrace", style="terrace.TCheckbutton")


    terrace.place(x=21, y=315, width=120, height=30)

    style.configure("garden.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("garden.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    garden = ttk.Checkbutton(master=frame_left, text="Garden", style="garden.TCheckbutton")


    garden.place(x=21, y=273, width=120, height=30)

    style.configure("balcony.TCheckbutton", background="#E4E2E2", foreground="#000")
    style.map("balcony.TCheckbutton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    balcony = ttk.Checkbutton(master=frame_left, text="Balcony", style="balcony.TCheckbutton")


    balcony.place(x=21, y=231, width=120, height=30)

    style.configure("balcony_size.TEntry", fieldbackground="#fff", foreground="#000")

    balcony_size = ttk.Entry(master=frame_left, style="balcony_size.TEntry")
    balcony_size.place(x=336, y=231, width=129, height=25)

    style.configure("garden_size.TEntry", fieldbackground="#fff", foreground="#000")

    garden_size = ttk.Entry(master=frame_left, style="garden_size.TEntry")
    garden_size.place(x=336, y=273, width=129, height=25)

    style.configure("terrace_size.TEntry", fieldbackground="#fff", foreground="#000")

    terrace_size = ttk.Entry(master=frame_left, style="terrace_size.TEntry")
    terrace_size.place(x=336, y=315, width=129, height=25)

    style.configure("loggia_size.TEntry", fieldbackground="#fff", foreground="#000")

    loggia_size = ttk.Entry(master=frame_left, style="loggia_size.TEntry")
    loggia_size.place(x=336, y=357, width=130, height=25)

    style.configure("wintergarden_size.TEntry", fieldbackground="#fff", foreground="#000")

    wintergarden_size = ttk.Entry(master=frame_left, style="wintergarden_size.TEntry")
    wintergarden_size.place(x=336, y=399, width=130, height=25)

    frame_right = tk.Frame(master=main)
    frame_right.config(bg="#BCBCBC")
    frame_right.place(x=650, y=26, width=600, height=450)

    frame_output = tk.Frame(master=frame_right)
    frame_output.config(bg="#EDECEC")
    frame_output.place(x=26, y=234, width=546, height=198)

    style.configure("living_area.TEntry", fieldbackground="#fff", foreground="#000")

    living_area = ttk.Entry(master=frame_right, style="living_area.TEntry")
    living_area.place(x=26, y=26, width=155, height=25)

    style.configure("rooms.TEntry", fieldbackground="#fff", foreground="#000")

    rooms = ttk.Entry(master=frame_right, style="rooms.TEntry")
    rooms.place(x=26, y=78, width=155, height=25)

    style.configure("address.TEntry", fieldbackground="#fff", foreground="#000")

    address = ttk.Entry(master=frame_right, style="address.TEntry")
    address.place(x=26, y=182, width=313, height=25)

    style.configure("postcode.TEntry", fieldbackground="#fff", foreground="#000")

    postcode = ttk.Entry(master=frame_right, style="postcode.TEntry")
    postcode.place(x=26, y=130, width=155, height=25)

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


    # Predict Button
    style.configure("button1.TButton", background="#E4E2E2", foreground="#000")
    style.map("button1.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

    button1 = ttk.Button(master=frame_right, text="Predict", style="button1.TButton")
    button1.place(x=495, y=176, width=80, height=40)

    # Living Area
    tk.Label(frame_right, text="Living Area:", bg="#BCBCBC").place(x=26, y=6)
    living_area = ttk.Entry(master=frame_right, style="living_area.TEntry")
    living_area.place(x=26, y=26, width=155, height=25)

    # Rooms
    tk.Label(frame_right, text="Rooms:", bg="#BCBCBC").place(x=26, y=58)
    rooms = ttk.Entry(master=frame_right, style="rooms.TEntry")
    rooms.place(x=26, y=78, width=155, height=25)

    # Postcode
    tk.Label(frame_right, text="Postcode:", bg="#BCBCBC").place(x=26, y=110)
    postcode = ttk.Entry(master=frame_right, style="postcode.TEntry")
    postcode.place(x=26, y=130, width=155, height=25)

    # Address
    tk.Label(frame_right, text="Address:", bg="#BCBCBC").place(x=26, y=162)
    address = ttk.Entry(master=frame_right, style="address.TEntry")
    address.place(x=26, y=182, width=313, height=25)

    # Balcony Size:
    tk.Label(frame_left, text="Balcony Size:", bg="#BCBCBC").place(x=200, y=231)
    balcony_size = ttk.Entry(master=frame_left, style="balcony_size.TEntry")
    balcony_size.place(x=335, y=231, width=130, height=25)

    # Garden Size:
    tk.Label(frame_left, text="Garden Size:", bg="#BCBCBC").place(x=200, y=273)
    garden_size = ttk.Entry(master=frame_left, style="garden_size.TEntry")
    garden_size.place(x=336, y=273, width=130, height=25)

    # Terrace Size:
    tk.Label(frame_left, text="Terrace Size:", bg="#BCBCBC").place(x=200, y=315)
    terrace_size = ttk.Entry(master=frame_left, style="terrace_size.TEntry")
    terrace_size.place(x=336, y=315, width=130, height=25)

    # Loggia Size:
    tk.Label(frame_left, text="Loggia Size:", bg="#BCBCBC").place(x=200, y=357)
    loggia_size = ttk.Entry(master=frame_left, style="loggia_size.TEntry")
    loggia_size.place(x=336, y=357, width=130, height=25)

    # Wintergarden Size:
    tk.Label(frame_left, text="Wintergarden Size:", bg="#BCBCBC").place(x=200, y=399)
    wintergarden_size = ttk.Entry(master=frame_left, style="wintergarden_size.TEntry")
    wintergarden_size.place(x=336, y=399, width=130, height=25)

    # Heating Source dropdown
    tk.Label(frame_left, text="Heating Source:", bg="#BCBCBC").place(x=336, y=26)
    heating_source_var = tk.StringVar()
    heating_source = ttk.Combobox(
        frame_left,
        textvariable=heating_source_var,
        state="readonly",
        values=["Select", "Oil", "Electric", "Gas"]
    )
    heating_source.place(x=336, y=51, width=155, height=25)
    heating_source.current(0)

    # Heating Type dropdown
    tk.Label(frame_left, text="Heating Type:", bg="#BCBCBC").place(x=336, y=85)
    heating_type_var = tk.StringVar()
    heating_type = ttk.Combobox(
        frame_left,
        textvariable=heating_type_var,
        state="readonly",
        values=["Select", "Floor", "Central", "Ceiling", "Oven", "Infrared"]
    )
    heating_type.place(x=336, y=110, width=155, height=25)
    heating_type.current(0)


    # --- HWB / fgEE Block ---
    # HWB + fgEE
    tk.Label(frame_right, text="HWB:", bg="#BCBCBC").place(x=200, y=6)
    hwb = ttk.Entry(frame_right)
    hwb.place(x=200, y=26, width=120, height=25)

    tk.Label(frame_right, text="fgEE:", bg="#BCBCBC").place(x=340, y=6)
    fgee = ttk.Entry(frame_right)
    fgee.place(x=340, y=26, width=120, height=25)


    # HWB Class + fgEE Class
    tk.Label(frame_right, text="HWB Class:", bg="#BCBCBC").place(x=200, y=58)
    hwb_class = ttk.Entry(frame_right)
    hwb_class.place(x=200, y=78, width=120, height=25)

    tk.Label(frame_right, text="fgEE Class:", bg="#BCBCBC").place(x=340, y=58)
    fgee_class = ttk.Entry(frame_right)
    fgee_class.place(x=340, y=78, width=120, height=25)

    # --- Property Type Dropdown (dynamic) ---
    property_type_var = tk.StringVar()
    property_type_label = tk.Label(frame_right, text="Property Type:", bg="#BCBCBC")
    property_type_dropdown = ttk.Combobox(
        frame_right,
        textvariable=property_type_var,
        state="readonly"
    )
    apartment_types = [
        "Select",
        "Roof Apartment", "Ground Floor Apartment", "Garconniere",
        "Coop Apartment", "Maisonette", "Penthouse", "Apartment", "Room"
    ]
    house_types = [
        "Select"
        "Multifamily House", "Single Family House", "Landhaus",
        "Villa", "Double House", "Castle/Chalet",
        "Row House", "Mountain Cabin", "Farmer House", "Cooperative House"
    ]
    def update_property_dropdown():
        val = apt_var.get()

        if val == 0:  # Apartment
            property_type_dropdown["values"] = apartment_types
            property_type_dropdown.current(0)

            property_type_label.place(x=200, y=110)
            property_type_dropdown.place(x=200, y=130, width=200, height=25)

        elif val == 1:  # House
            property_type_dropdown["values"] = house_types
            property_type_dropdown.current(0)

            property_type_label.place(x=200, y=110)
            property_type_dropdown.place(x=200, y=130, width=200, height=25)

        else:
            property_type_label.place_forget()
            property_type_dropdown.place_forget()

    apt_var.trace_add("write", lambda *args: update_property_dropdown())
    update_property_dropdown()

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

    main.mainloop()


def backendRun():
    threading.Thread(target=_backendRun).start()


def _backendRun():
    if scraping.get():
        clean_data.set(True)
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
