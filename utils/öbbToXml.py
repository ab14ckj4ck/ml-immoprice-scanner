import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time, random
from geopy.geocoders import Nominatim

BASE_URL = "https://bahnhof.oebb.at"
INPUT_FILE = "trainStationInput.txt"

HEADERS = {"User-Agent": "Mozilla/5.0"}
geolocator = Nominatim(user_agent="oebb_scraper")


# =========================
# LINKS AUS TXT EXTRAHIEREN
# =========================
def extract_links_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        # nur echte stationslinks
        if href.startswith("/de/") and href.count("/") == 3:
            links.append(BASE_URL + href)

    links = sorted(set(links))

    print(f"[INFO] Found {len(links)} links")

    return links


# =========================
# STATION PARSEN
# =========================
def parse_station(url):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]),
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8",
        "Connection": "keep-alive"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    h1 = soup.find("h1")
    if not h1:
        return None, None

    name = h1.text.strip()

    container = soup.find("div", {"data-area-content": "stationOverview"})
    if not container:
        return name, None

    p = container.find("p")
    if not p:
        return name, None

    for br in p.find_all("br"):
        br.replace_with("\n")

    lines = [l.strip() for l in p.get_text().split("\n") if l.strip()]

    # Erwartet:
    # ["9520 Mittlern", "Mittlern Bahnhofstraße 15", "Kärnten"]

    if len(lines) < 2:
        return name, None

    # 🔥 WICHTIG: richtige Reihenfolge bauen
    address = f"{lines[1]}, {lines[0]}, Austria"

    return name, address


# =========================
# GEOCODING
# =========================
def get_coordinates(address):
    try:
        loc = geolocator.geocode(address, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass

    return None, None


# =========================
# XML
# =========================
def build_xml(stations, filename="train-stations.xml"):
    root = ET.Element("train_stations")

    for s in stations:
        station = ET.SubElement(root, "station")
        station.set("name", s["name"])

        ET.SubElement(station, "lat").text = str(s["lat"])
        ET.SubElement(station, "lon").text = str(s["lon"])

    ET.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)


# =========================
# MAIN
# =========================
def main():
    links = extract_links_from_file(INPUT_FILE)

    stations = []

    for url in links:
        try:
            name, address = parse_station(url)

            if not address:
                continue

            print(f"[ADDR] {name} -> {address}")

            lat, lon = get_coordinates(address)

            if lat is None:
                print(f"[MISS] {name}")
                continue

            stations.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })

            print(f"  -> {name}")

            time.sleep(1)  # rate limit

        except Exception as e:
            print(f"ERROR: {url} -> {e}")

    build_xml(stations)


if __name__ == "__main__":
    main()