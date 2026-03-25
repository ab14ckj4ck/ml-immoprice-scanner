import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from geopy.geocoders import Nominatim

BASE_URL = "https://bahnhof.oebb.at"
STATES = [
    "kaernten",
    "oberoesterreich",
    "niederoesterreich",
    "steiermark",
    "tirol",
    "salzburg",
    "vorarlberg",
    "wien",
    "burgenland"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

geolocator = Nominatim(user_agent="oebb_scraper")


# -------------------------------
# STEP 1: alle detail links holen
# -------------------------------
def get_station_links(state):
    url = f"{BASE_URL}/de/{state}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []

    nav = soup.find("ul", class_="pn-list")
    if not nav:
        return []

    for a in nav.find_all("a", href=True):
        href = a["href"]

        # nur echte station links
        if href.startswith(f"/de/{state}/"):
            links.append(BASE_URL + href)

    return list(set(links))


# -------------------------------
# STEP 2: name + adresse holen
# -------------------------------
def parse_station(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    name = soup.find("h1").text.strip()
    container = soup.find("div", {"data-area-content": "stationOverview"})
    if not container:
        return name, None

    p = container.find("p")
    if not p:
        return name, None

    for br in p.find_all("br"):
        br.replace_with("\n")

    lines = [line.strip() for line in p.get_text().split("\n") if line.strip()]
    address = ", ".join(lines)

    return name, address


# -------------------------------
# STEP 3: geocoding
# -------------------------------
def get_coordinates(address):
    try:
        location = geolocator.geocode(address + ", Austria", timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass

    return None, None


# -------------------------------
# STEP 4: XML bauen
# -------------------------------
def build_xml(stations):
    root = ET.Element("train_stations")

    for s in stations:
        station = ET.SubElement(root, "station")
        station.set("name", s["name"])

        ET.SubElement(station, "lat").text = str(s["lat"])
        ET.SubElement(station, "lon").text = str(s["lon"])

    tree = ET.ElementTree(root)
    tree.write("train-stations.xml", encoding="utf-8", xml_declaration=True)


# -------------------------------
# MAIN
# -------------------------------
def main():
    stations = []

    for state in STATES:
        print(f"[+] {state}")
        links = get_station_links(state)

        for link in links:
            try:
                name, address = parse_station(link)

                lat, lon = get_coordinates(address)

                if lat is not None:
                    stations.append({
                        "name": name,
                        "lat": lat,
                        "lon": lon
                    })
                    print(f"  -> {name}")

                time.sleep(1)  # wichtig wegen rate limit

            except Exception as e:
                print(f"ERROR: {link} -> {e}")

    build_xml(stations)


if __name__ == "__main__":
    main()