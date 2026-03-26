from mlModels.regression.data.data import getRegressionData
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor as xgbr
import numpy as np
import pandas as pd
import logging


CV = True
CV_FOLDS = 5

logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# noinspection DuplicatedCode
def buyPriceXgbrModel(df, drop_cols, accommodation="house", k=2):
    """
    Trains and evaluates an XGBoost Regressor for rental prices.

    Args:
        df (pd.DataFrame): The input dataset containing real estate features.
        drop_cols (list): Initial list of columns to drop from the apartment dataset.
        accommodation (str): Type of property to model ("house" or "apt"). Defaults to "house".
        k (int): Cluster identifier used for logging purposes. Defaults to 2.

    Returns:
        Model: returns a trained model

        Prints evaluation metrics (MAE, RMSE, R2) and feature importances to the console.
    """
    df_house_X, df_house_y, df_apt_X, df_apt_y = getRegressionData(df)

    df_apt_X.drop(columns=drop_cols, inplace=True, errors="ignore")
    df_apt_X.drop(columns=drop_cols, inplace=True, errors="ignore")

    X, y = None, None

    if accommodation == "house":
        X = df_house_X
        y = df_house_y
    elif accommodation == "apt":
        X = df_apt_X
        y = df_apt_y

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    drop_cols = ["finance_type", "loc_14_7", "loc_14_8", "is_ab", "is_rh", "is_dhh",
                 "is_sbc", "is_villa", "log_wintergarden_size", "is_gh", "is_bh",
                 "loc_14_6", "wintergarden_ratio", "estate_ratio", "fgee", "is_ceiling", "has_kitchen", "is_bio",
                 "is_electro", "loc_14_10"]

    X_train.drop(columns=drop_cols, inplace=True, errors="ignore")
    X_test.drop(columns=drop_cols, inplace=True, errors="ignore")

    model = xgbr(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    if CV:
        scores = cross_val_score(model, X_train, y_train, cv=CV_FOLDS, scoring="r2", verbose=True)
        logging.info(f"-------[BUY] Cross Validation Scores for K={k}-------")
        logging.info(f"CV R2 Scores: {scores}")
        logging.info(f"Mean R2 Score: {scores.mean():.4f}")
        logging.info(f"Standard Deviation: {scores.std():.4f}")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    logging.info(f"-------[BUY] XGBoost Regression Results for K={k}-------")
    logging.info(f"MAE:  {mae:.4f}")
    logging.info(f"RMSE: {rmse:.4f}")
    logging.info(f"R2:   {r2:.4f}\n")

    return model