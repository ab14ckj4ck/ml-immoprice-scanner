import os
from dotenv import load_dotenv
import psycopg2
import warnings

warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy connectable"
)

load_dotenv("database/.env")

def getConnection():
    """
    Establishes and returns a connection to the PostgreSQL database using environment variables.

    :return: A psycopg2 connection object.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )