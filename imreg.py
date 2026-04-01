from scraper.source1_scraper import baseScraper
from datamanipulation.austriaFeatureEngineering import engineerFeatures
import logging

def main(SOURCE_1=True, SCRAPE_SOURCE_1=False, CLEAN_DATA=True, MODELS=False, PAGES=100, ROWS=100):
    """
    Main entry point for the scraper application.

    If SOURCE 1 is enabled, it optionally scrapes new data from source 1
    using the baseScraper and then performs data cleaning on the results
    based on defined house and apartment types.
    """
    asciiArt()
    logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')

    if SOURCE_1:
        if SCRAPE_SOURCE_1:
            logging.info(f"Starting Source 1 Scraper with {PAGES} pages and {ROWS} rows")
            baseScraper(pages=PAGES, scrape_details=True, rows=ROWS)
            logging.info("Finished scraping Source 1")

    if CLEAN_DATA:
        logging.info("Starting Source 1 Data Cleaning")
        engineerFeatures()
        logging.info("Finished Source 1 Data Cleaning")

    if MODELS:
        logging.info("Starting Models")

def asciiArt():
    print(r".___                        _________                                  ")
    print(r"|   | _____   _____   ____ /   _____/ ________________  ______   ____  ")
    print(r"|   |/     \ /     \ /  _ \\_____  \_/ ___\_  __ \__  \ \____ \_/ __ \ ")
    print(r"|   |  Y Y  \  Y Y  (  <_> )        \  \___|  | \// __ \|  |_> >  ___/ ")
    print(r"|___|__|_|  /__|_|  /\____/_______  /\___  >__|  (____  /   __/ \___  >")
    print(r"          \/      \/              \/     \/           \/|__|        \/ ")

if __name__ == "__main__":
    main()