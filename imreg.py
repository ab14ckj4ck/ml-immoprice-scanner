from scraper.source1_scraper import baseScraper
from datamanipulation.cleanData import cleanData

SOURCE_1 = True
SCRAPE_SOURCE_1 = False
SOURCE_1_HOUSE_TYPES = {
    "Bungalow", "Mehrfamilienhaus", "Einfamilienhaus", "Landhaus", "Villa",
    "Doppelhaushälfte", "Schloss/Burg/Chalet", "Reihenhaus",
    "Almhütte/Berghütte", "Bauernhaus", "Genossenschaftshaus"
}
SOURCE_1_APARTMENT_TYPES = {
    "Dachgeschoßwohnung", "Erdgeschoßwohnung", "Garconniere",
    "Genossenschaftswohnung", "Maisonette", "Penthauswohnung",
    "Wohngung", "Zimmer/WG"
}

def main():
    """
    Main entry point for the scraper application.

    If SOURCE 1 is enabled, it optionally scrapes new data from source 1
    using the baseScraper and then performs data cleaning on the results
    based on defined house and apartment types.
    """
    if SOURCE_1:
        if SCRAPE_SOURCE_1:
            print("\n-------Starting Source 1 Scraper-------")
            baseScraper(pages=7, scrape_details=True, rows=100)

        print("\n-------Starting Source 1 Data Cleaning-------")
        cleanData()

if __name__ == "__main__":
    main()