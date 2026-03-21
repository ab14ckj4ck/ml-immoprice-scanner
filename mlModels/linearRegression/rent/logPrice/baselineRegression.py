from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def linearRegression(df_y, df_X, CV=False, folds=5, verbose=False, random_state=42, scoring="r2"):
    """
    Performs linear regression on the provided dataset and prints evaluation metrics.

    Args:
        df_y (pd.Series or np.array): Target variable (e.g., log-transformed prices).
        df_X (pd.DataFrame or np.array): Feature matrix.
        CV (bool, optional): If True, performs 5-fold cross-validation on the training set.
                             Defaults to False.
        folds (int, optional): Number of folds for cross-validation. Only used if CV is True.
                               Defaults to 5.
        verbose (bool, optional): If True, prints cross-validation details. Defaults to False.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.
        scoring (str, optional): Scoring metric for cross-validation. Defaults to "r2".

    Returns:
        None: Prints results to the console.
    """
    print(df_y.describe())
    X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.2, random_state=42)

    model = LinearRegression()

    if CV:
        scores = cross_val_score(model, X_train, y_train, cv=folds, scoring=scoring, verbose=verbose)
        print("\n-------Cross Validation Scores-------")
        print(f"CV R2 Scores: {scores}")
        print(f"Mean R2 Score: {scores.mean():.4f}")
        print(f"Standard Deviation: {scores.std():.4f}")
        print()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("-------Linear Regression Results-------")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2:   {r2:.4f}")
    print()