from mlModels.kmeans.runCluster import runCluster
from mlModels.regression.rent.logPrice.rentPriceXgbrModel import rentPriceXgbrModel
from mlModels.regression.buy.logPrice.buyPriceXgbrModel import buyPriceXgbrModel
from mlModels.regression.data.data import getData
import logging, joblib

REGRESSION = True
CV_FOLDS = 5
HOUSES = True
APARTMENTS = True
RENT = True
BUY = True

DROP_COLS_APT = ["is_mfh", "is_efh", "is_lh", "is_villa", "is_dhh",
                 "is_sbc", "is_rh", "is_ab", "is_bh", "is_gh"]

DROP_COLS_HOUSE = ["is_dgw", "is_egw", "is_gc", "is_gw", "is_ms", "is_phw", "is_apt", "is_wg"]

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def runModels():
    """
    Executes the linear regression models for both houses and apartments.

    Loads the data, splits it into features and targets, and runs the regression with cross-validation.
    """
    if REGRESSION:
        df_rent_features = getData(filter_type="finance_type", filter_val="rent", table="rent_features")
        rent_cluster_data = runCluster()
        df_rent_log_features = df_rent_features.merge(rent_cluster_data, on="id")  # k=4 tested for K-Means

        df_buy_features = getData(filter_type="finance_type", filter_val="buy", table="buy_features")
        buy_cluster_data = runCluster()
        df_buy_log_features = df_buy_features.merge(buy_cluster_data, on="id") # k=14 tested for K-Means

        if HOUSES:
            logging.info("Starting XGBR logPrice Houses")
            if RENT:
                logging.info("-------XGBR Rent logPrice Houses-------")
                rent_house_model = rentPriceXgbrModel(df=df_rent_log_features, drop_cols=DROP_COLS_HOUSE, accommodation="house", k=14)
                joblib.dump(rent_house_model, "mlModels/regression/data/rent_house_model.pkl")
            if BUY:
                logging.info("-------XGBR Buy logPrice Houses-------")
                buy_house_model = buyPriceXgbrModel(df=df_buy_log_features, drop_cols=DROP_COLS_HOUSE, accommodation="house", k=14)
                joblib.dump(buy_house_model, "mlModels/regression/data/buy_house_model.pkl")

            logging.info("Finished XGBR logPrice Houses")

        if APARTMENTS:
            logging.info("Starting XGBR logPrice Apartments")
            if RENT:
                logging.info("-------XGBR Rent logPrice Apartments-------")
                rent_apt_model = rentPriceXgbrModel(df=df_rent_log_features, drop_cols=DROP_COLS_APT, accommodation="apt", k=14)
                joblib.dump(rent_apt_model, "mlModels/regression/data/rent_apt_model.pkl")
            if BUY:
                logging.info("-------XGBR Buy logPrice Apartments-------")
                buy_apt_model = buyPriceXgbrModel(df=df_buy_log_features, drop_cols=DROP_COLS_APT, accommodation="apt", k=14)
                joblib.dump(buy_apt_model, "mlModels/regression/data/buy_apt_model.pkl")

            logging.info("Finished XGBR logPrice Apartments")