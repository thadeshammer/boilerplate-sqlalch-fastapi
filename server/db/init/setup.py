import time

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

from server.db.common import Base

# TODO home these constants in configuration
DATABASE_URL = URL.create(drivername="postgresql",
                          username="myuser",
                          password="mypassword",
                          host="postgres",
                          database="default_database",
                          port=5432)

MAX_RETRIES = 5
RETRY_INTERVAL = 5


def db_init():
    """Init DB and return the session instance, creating tables (in models) if they don't yet exist.

    Returns:
        The db session object.
    """
    retries = 0

    # This app is much lighter weight than most DBs so it will win the race usually.
    while retries < MAX_RETRIES:
        try:
            engine = create_engine(DATABASE_URL)
            # Creates mapped classes as tables if they don't exist
            Base.metadata.create_all(engine)

            print("DB connect success.")
            return engine
        except OperationalError as e:
            print(f"Error connecting to the database on try {retries}: {e}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {RETRY_INTERVAL} seconds...")
                time.sleep(RETRY_INTERVAL)
            else:
                print("Max retries exceeded. Exiting.")
                raise
