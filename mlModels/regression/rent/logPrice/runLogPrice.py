from mlModels.regression.rent.logPrice.xgbrModel import xgboost
import logging

REGRESSION = True
CV_FOLDS = 5
HOUSES = False
APARTMENTS = True

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def runModels():
    """
    Executes the linear regression models for both houses and apartments.

    Loads the data, splits it into features and targets, and runs the regression with cross-validation.
    """
    if REGRESSION:
        if HOUSES:
            logging.info("Starting XGBR Houses")
            print("\n-------XGBR Houses-------")

        if APARTMENTS:
            logging.info("Starting XGBR Apartments")
            print("\n-------XGBR Apartments-------")
            xgboost()
