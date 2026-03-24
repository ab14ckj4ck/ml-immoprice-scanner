from mlModels.regression.rent.logPrice.data import getData, getRegressionData
from mlModels.kmeans.rent.runCluster import runCluster
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor as xgbr
import numpy as np
import pandas as pd

CV = True
CV_VAL = 5

def xgboost():
    df_features = getData()
    cluster_dict = runCluster()

    for k, df_cluster in cluster_dict.items():
        df = df_features.merge(df_cluster, on="id", how="inner")
        df_house_X, df_house_y, df_apt_X, df_apt_y = getRegressionData(df)
        df_apt_X = df_apt_X.drop(columns=["is_mfh", "is_efh", "is_lh", "is_villa", "is_dhh",
                                          "is_sbc", "is_rh", "is_ab", "is_bh", "is_gh"])

        X_train, X_test, y_train, y_test = train_test_split(df_apt_X, df_apt_y, test_size=0.2, random_state=42)

        drop_cols = ["is_wg", "is_phw", "is_ceiling", "is_electro", "has_kitchen",
                     "estate_ratio", "log_wintergarden_size", "is_bio", "fgee",
                     "wintergarden_ratio", "loc_14_6", "has_wintergarden", "loc_14_7",
                     "is_geothermal", "loc_14_8", "is_photovoltaik", "is_oven", "is_gw", "is_gc",
                     "loc_14_4", "loc_14_13", "is_urban", "loc_14_5", "loc_14_10", "loc_14_2",
                     "is_infrared", "is_central", "loc_14_11", "loc_14_0", "is_ms", "is_pellets",
                     "is_oil", "is_air_heating", "loc_14_3", "loc_14_1", "is_dgw", "log_garden_size",
                     "has_garden", "log_loggia_size", "has_loggia", "loc_14_12", "is_apt", "is_egw",
                     "has_balcony", "garden_ratio", "has_carport", "has_closet", "has_cellar"]

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
            scores = cross_val_score(model, X_train, y_train, cv=CV_VAL, scoring="r2", verbose=True)
            print(f"\n-------Cross Validation Scores for K={k}-------")
            print(f"CV R2 Scores: {scores}")
            print(f"Mean R2 Score: {scores.mean():.4f}")
            print(f"Standard Deviation: {scores.std():.4f}")
            print()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        print(f"-------XGBoost Regression Results for K={k}-------")
        print(f"MAE:  {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2:   {r2:.4f}")
        importance_df = pd.DataFrame({
            "feature" : X_train.columns,
            "importance" : model.feature_importances_
        })
        importance_df = importance_df.sort_values("importance", ascending=False)
        print(importance_df.tail(20))
        print()
