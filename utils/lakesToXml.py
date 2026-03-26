import json
import xml.etree.ElementTree as ET
import numpy as np

# =========================
# CONFIG
# =========================
INPUT_FILE = "lake_carinthia.json"
OUTPUT_FILE = "lakes_pois.xml"

MIN_SIZE_DEG = 0.02   # ~2km
MAX_POINTS = 6


# =========================
# HELPERS
# =========================
def is_large_lake(geometry):
    if not geometry:
        return False

    lats = [p["lat"] for p in geometry]
    lons = [p["lon"] for p in geometry]

    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)

    return lat_range > MIN_SIZE_DEG or lon_range > MIN_SIZE_DEG


def sample_points(geometry):
    n = len(geometry)

    k = max(1, min(MAX_POINTS, n // 20))

    indices = np.linspace(0, n - 1, k, dtype=int)
    return [geometry[i] for i in indices]


def get_geometry(el, way_map):
    # -------------------------
    # WAY → direkt
    # -------------------------
    if el["type"] == "way":
        return el.get("geometry", [])

    # -------------------------
    # RELATION → aus ways bauen
    # -------------------------
    if el["type"] == "relation":
        coords = []

        for m in el.get("members", []):
            if m.get("type") != "way":
                continue

            way = way_map.get(m.get("ref"))
            if not way:
                continue

            geom = way.get("geometry")
            if geom:
                coords.extend(geom)

        return coords

    return []


def is_lake(tags):
    if tags.get("natural") != "water":
        return False

    # Flüsse raus
    water_type = tags.get("water")

    if water_type == "river" or water_type == "reservoir" or not water_type:
        return False

    return True


# =========================
# MAIN
# =========================
def main():
    print("[INFO] Loading JSON...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = data["elements"]
    print(f"[INFO] Elements: {len(elements)}")

    # Map für relation → way lookup
    way_map = {
        el["id"]: el
        for el in elements
        if el["type"] == "way"
    }

    root = ET.Element("pois")

    seen_points = set()

    total_lakes = 0
    total_points = 0

    for idx, el in enumerate(elements):

        if idx % 10000 == 0 and idx > 0:
            print(f"[PROGRESS] {idx}/{len(elements)}")

        if el.get("type") not in ["way", "relation"]:
            continue

        tags = el.get("tags", {})

        if not is_lake(tags):
            continue

        geometry = get_geometry(el, way_map)

        if not geometry:
            continue

        if not is_large_lake(geometry):
            continue

        name = tags.get("name", "lake")

        sampled = sample_points(geometry)

        if not sampled:
            continue

        total_lakes += 1

        for i, p in enumerate(sampled):
            lat = round(p["lat"], 6)
            lon = round(p["lon"], 6)

            # Dedup
            if (lat, lon) in seen_points:
                continue

            seen_points.add((lat, lon))

            poi = ET.SubElement(root, "poi")
            poi.set("name", f"{name}_{i}")

            ET.SubElement(poi, "lat").text = str(lat)
            ET.SubElement(poi, "lon").text = str(lon)

            total_points += 1

    ET.ElementTree(root).write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

    print(f"[DONE] Lakes: {total_lakes}")
    print(f"[DONE] Unique POIs: {total_points}")
    print(f"[FILE] {OUTPUT_FILE}")


if __name__ == "__main__":
    main()