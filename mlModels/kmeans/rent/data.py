from database.db import get_connection
import pandas as pd


def getData():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM listings", conn)

    df = df[
        [
            "id", "lat", "lon"
        ]
    ]
    conn.close()
    return df
