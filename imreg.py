from scraper.source1_scraper import baseScraper
from datamanipulation.cleanData import cleanData
from mlModels.kmeans.rent.runCluster import runCluster
from mlModels.regression.rent.logPrice.runLogPrice import runModels
import logging

SOURCE_1 = False
SCRAPE_SOURCE_1 = False
MODELS = True

def main():
    """
    Main entry point for the scraper application.

    If SOURCE 1 is enabled, it optionally scrapes new data from source 1
    using the baseScraper and then performs data cleaning on the results
    based on defined house and apartment types.
    """

    logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s')

    if SOURCE_1:
        if SCRAPE_SOURCE_1:
            logging.info("Starting Source 1 Scraper")
            print("\n-------Starting Source 1 Scraper-------")
            baseScraper(pages=12, scrape_details=True, rows=100)
            logging.info("Finished scraping Source 1")

        logging.info("Starting Source 1 Data Cleaning")
        print("\n-------Starting Source 1 Data Cleaning-------")
        cleanData()
        logging.info("Finished Source 1 Data Cleaning")

    if MODELS:
        logging.info("Starting Models")
        runModels()

if __name__ == "__main__":
    main()