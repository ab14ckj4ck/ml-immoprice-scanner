from database.db import getConnection
import pandas as pd


def getData():
    conn = getConnection()
    df = pd.read_sql("SELECT * FROM listings", conn)

    df = df[
        [
            "id", "lat", "lon"
        ]
    ]
    conn.close()
    return df
