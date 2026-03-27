from mlModels.kmeans.runCluster import runCluster
from mlModels.regression.rent.OUTDATEDlogPrice.rentPriceXgbrModel import rentPriceXgbrModel
from mlModels.regression.buy.OUTDATEDlogPrice.buyPriceXgbrModel import buyPriceXgbrModel
from mlModels.regression.data.data import getData
from utils.enums import ModelParam, Mappings, Listings
import logging, joblib



logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def runModels():
    """
    Executes the linear regression models for both houses and apartments.

    Loads the data, splits it into features and targets, and runs the regression with cross-validation.
    """
    if ModelParam.REGRESSION:
        df_rent_features = getData(filter_type=Listings.FINANCE_TYPE, filter_val=Listings.RENT)
        rent_cluster_data = runCluster()
        df_rent_features = df_rent_features.merge(rent_cluster_data, on=Listings.ID)

        df_buy_features = getData(filter_type=Listings.FINANCE_TYPE, filter_val=Listings.BUY)
        buy_cluster_data = runCluster()
        df_buy_features = df_buy_features.merge(buy_cluster_data, on=Listings.ID)

        if ModelParam.HOUSES:
            logging.info("Starting XGBR OUTDATEDlogPrice Houses")
            if ModelParam.RENT:
                logging.info("-------XGBR Rent OUTDATEDlogPrice Houses-------")

                joblib.dump(rent_house_model, "mlModels/regression/data/rent_house_model.pkl")
            if ModelParam.BUY:
                logging.info("-------XGBR Buy OUTDATEDlogPrice Houses-------")

                joblib.dump(buy_house_model, "mlModels/regression/data/buy_house_model.pkl")

            logging.info("Finished XGBR OUTDATEDlogPrice Houses")

        if ModelParam.APARTMENTS:
            logging.info("Starting XGBR OUTDATEDlogPrice Apartments")
            if ModelParam.RENT:
                logging.info("-------XGBR Rent OUTDATEDlogPrice Apartments-------")

                joblib.dump(rent_apt_model, "mlModels/regression/data/rent_apt_model.pkl")
            if ModelParam.BUY:
                logging.info("-------XGBR Buy OUTDATEDlogPrice Apartments-------")

                joblib.dump(buy_apt_model, "mlModels/regression/data/buy_apt_model.pkl")

            logging.info("Finished XGBR OUTDATEDlogPrice Apartments")