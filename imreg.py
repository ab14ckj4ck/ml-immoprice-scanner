from scraper.source1_scraper import baseScraper
from datamanipulation.cleanData import cleanData
from mlModels.linearRegression.rent.logPrice.runLR import runModels

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
    if SOURCE_1:
        if SCRAPE_SOURCE_1:
            print("\n-------Starting Source 1 Scraper-------")
            baseScraper(pages=7, scrape_details=True, rows=100)

        print("\n-------Starting Source 1 Data Cleaning-------")
        cleanData()

    if MODELS:
        runModels()

if __name__ == "__main__":
    main()