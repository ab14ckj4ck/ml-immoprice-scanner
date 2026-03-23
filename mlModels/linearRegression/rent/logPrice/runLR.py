from mlModels.linearRegression.rent.logPrice.data import getData, getLinearRegressionData
from mlModels.linearRegression.rent.logPrice.baselineRegression import linearRegression
import logging

LINEAR_REGRESSION = True
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
    if LINEAR_REGRESSION:
        logging.info("Starting Linear Regression")
        print("\n-------Starting Linear Regression-------\n")
        df = getData()
        df_house_X, df_house_y, df_apt_X, df_apt_y = getLinearRegressionData(df)

        if HOUSES:
            logging.info("Starting LR Houses")
            print("\n-------LR Houses-------")
            linearRegression(df_house_y, df_house_X, CV=True, folds=CV_FOLDS)

        if APARTMENTS:
            logging.info("Starting LR Apartments")
            print("\n-------LR Apartments-------")
            linearRegression(df_apt_y, df_apt_X, CV=True, folds = CV_FOLDS)
