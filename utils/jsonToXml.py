import json
import xml.etree.ElementTree as ET
import os

# 👉 deine Dateien (anpassen falls nötig)
INPUT_FILES = [
    "mall.json",
    "park.json",
    "peak.json",
    "sport_centre.json",
    "tourist.json"
]

OUTPUT_FILE = "../data/pois.xml"


def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)["elements"]


def main():
    all_pois = []
    seen = set()

    total_files = len(INPUT_FILES)

    for file_idx, file in enumerate(INPUT_FILES, start=1):
        print(f"[{file_idx}/{total_files}] Loading {file}...")

        if not os.path.exists(file):
            print(f"[WARN] File not found: {file}")
            continue

        elements = load_json(file)
        total_elements = len(elements)

        print(f"    -> {total_elements} entries")

        for i, el in enumerate(elements):
            # Progress alle 5000 Einträge
            if i % 5000 == 0 and i > 0:
                print(f"    [{file}] {i}/{total_elements}")

            # Nur Nodes
            if el.get("type") != "node":
                continue

            tags = el.get("tags", {})

            # Name Pflicht
            name = tags.get("name")
            if not name:
                continue

            lat = el.get("lat")
            lon = el.get("lon")

            if lat is None or lon is None:
                continue

            # Dedup (wichtig!)
            key = (round(lat, 4), round(lon, 4))
            if key in seen:
                continue
            seen.add(key)

            all_pois.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })

        print(f"    -> done {file}")

    print(f"\n[INFO] Total POIs after filtering: {len(all_pois)}")

    # =========================
    # XML BUILD
    # =========================
    print("[INFO] Writing XML...")

    root = ET.Element("pois")

    for idx, poi_data in enumerate(all_pois):
        if idx % 5000 == 0 and idx > 0:
            print(f"    Writing {idx}/{len(all_pois)}")

        poi = ET.SubElement(root, "poi")
        poi.set("name", poi_data["name"])

        ET.SubElement(poi, "lat").text = str(poi_data["lat"])
        ET.SubElement(poi, "lon").text = str(poi_data["lon"])

    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

    print(f"[DONE] Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()