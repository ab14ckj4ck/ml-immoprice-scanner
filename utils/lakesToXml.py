import requests
import time
import math
import xml.etree.ElementTree as ET
from collections import defaultdict

# =====================
# CONFIG
# =====================
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]

OUTPUT_FILE = "lakes.xml"
MIN_NODES = 6
MIN_DISTANCE = 0.01  # ~1km


# =====================
# FETCH WITH RETRY
# =====================
def fetch_with_retry(query, retries=15):
    for i in range(retries):
        try:
            url = OVERPASS_URLS[i % len(OVERPASS_URLS)]
            response = requests.post(url, data=query)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Retry {i+1}/{retries} failed:", e)
            time.sleep(2)

    raise Exception("Overpass failed after retries")


# =====================
# PARSE
# =====================
def parse_osm(elements):
    nodes = {}
    ways = {}
    relations = []

    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lat"], el["lon"])

        elif el["type"] == "way":
            ways[el["id"]] = el["nodes"]

        elif el["type"] == "relation":
            relations.append(el)

    return nodes, ways, relations


# =====================
# HELPERS
# =====================
def get_way_coords(way_id, ways, nodes):
    return [nodes[n] for n in ways.get(way_id, []) if n in nodes]


def get_relation_coords(rel, ways, nodes):
    coords = []
    for m in rel.get("members", []):
        if m["type"] == "way":
            coords.extend(get_way_coords(m["ref"], ways, nodes))
    return coords


def select_points(coords):
    if not coords:
        return []

    n_points = max(1, min(5, len(coords) // 50))

    indices = [
        int(i * len(coords) / n_points)
        for i in range(n_points)
    ]

    return [coords[i] for i in indices]


# =====================
# DISTANCE FILTER
# =====================
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def filter_points(points, min_dist):
    result = []

    for p in points:
        if all(distance(p, r) > min_dist for r in result):
            result.append(p)

    return result


# =====================
# EXTRACT
# =====================
def extract_pois(elements):
    nodes, ways, relations = parse_osm(elements)

    lakes = defaultdict(list)

    # Ways
    for el in elements:
        if el["type"] != "way":
            continue

        name = el.get("tags", {}).get("name")
        if not is_valid_lake(name):
            continue

        coords = get_way_coords(el["id"], ways, nodes)

        if len(coords) < MIN_NODES:
            continue

        for lat, lon in select_points(coords):
            lakes[name].append((lat, lon))

    # Relations
    for rel in relations:
        tags = rel.get("tags", {})

        if tags.get("type") != "multipolygon":
            continue

        name = tags.get("name")
        if not name:
            continue

        coords = get_relation_coords(rel, ways, nodes)

        if len(coords) < MIN_NODES:
            continue

        for lat, lon in select_points(coords):
            lakes[name].append((lat, lon))

    # Distance filtering per lake
    final_pois = []

    for name, points in lakes.items():
        filtered = filter_points(points, MIN_DISTANCE)

        for lat, lon in filtered:
            final_pois.append((name, lat, lon))

    return final_pois


# =====================
# XML
# =====================
def write_xml(pois):
    root = ET.Element("pois")

    for name, lat, lon in pois:
        poi = ET.SubElement(root, "poi", name=name)

        ET.SubElement(poi, "lat").text = str(lat)
        ET.SubElement(poi, "lon").text = str(lon)

    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)


def normalize(text):
    text = text.lower()
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def is_valid_lake(name):
    if not name:
        return False

    name = normalize(name)

    # ✅ explizit erlauben
    whitelist = [
        "badeteich",
    ]

    for w in whitelist:
        if w in name:
            return True

    # ❌ alles raus was Müll ist
    blacklist = [
        "becken",
        "klaer",
        "klaerteich",
        "klaerbecken",
        "klaergrube",
        "auffang",
        "biotop",
        "insel",
        "speicher",
        "rueckhalte",
        "teich",
        "weiher",
        "lagune",
        "hafen",
        "sandgrube",
        "lehmloecher",
        "garten",
        "fisch",
        "grundwasser",
        "brunnen",
        "frosch",
        "kroeten"
        "grube",
        "sicker",
        "graben"
    ]

    for b in blacklist:
        if b in name:
            return False

    return True


# =====================
# MAIN
# =====================
def main():
    all_pois = []

    for i in range(1, 10):
        QUERY = f"""
        [out:json][timeout:120];

        area["ISO3166-2"="AT-{i}"]->.searchArea;
        
        (
          way["natural"="water"]["name"]["water"!~"river|reservoir|basin|oxbow|pond|canal"]["natural"!~"shingle"]["leisure"!~"slipway"]["category"!~"slipway"]["place"!~"island|islet"](area.searchArea);
          relation["natural"="water"]["name"]["water"!~"river|reservoir|basin|oxbow|pond|canal"]["natural"!~"shingle"]["leisure"!~"slipway"]["category"!~"slipway"]["place"!~"island|islet"](area.searchArea);
        );
        (._;>;);
        out body;
        """

        print(f"Fetching AT-{i}...")

        try:
            data = fetch_with_retry(QUERY)
        except Exception as e:
            print("FAILED:", e)
            continue

        pois = extract_pois(data["elements"])
        print(f" → {len(pois)} POIs")

        all_pois.extend(pois)

        time.sleep(3)

    print(f"Total POIs: {len(all_pois)}")

    write_xml(all_pois)

    print("Done.")


if __name__ == "__main__":
    main()