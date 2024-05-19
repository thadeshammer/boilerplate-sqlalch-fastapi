import time
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from server.db.base import Base
from server.db.models import TestModel

# TODO home these constants in configuration
DATABASE_URL = URL(drivername="postgresql",
                   username="myuser",
                   password="mypassword",
                   host="postgres",
                   database="default_database",
                   port=5432)

MAX_RETRIES = 5
RETRY_INTERVAL = 5

_engine: Optional[Engine] = None
_session_local: Optional[sessionmaker] = None


def get_engine() -> Optional[Engine]:
    global _engine
    if _engine is None:
        retries = 0

        while retries < MAX_RETRIES and _engine is None:
            try:
                _engine = create_engine(DATABASE_URL)
                Base.metadata.create_all(_engine)
                print("DB connect success.")
            except OperationalError as e:
                print(
                    f"Error connecting to the database on try {retries}: {e}")
                retries += 1
                if retries < MAX_RETRIES:
                    print(f"Retrying in {RETRY_INTERVAL} seconds...")
                    time.sleep(RETRY_INTERVAL)
                else:
                    print("Max retries exceeded. Exiting.")
                    raise e

    return _engine


def get_session() -> Session:
    global _session_local
    if _session_local is None:
        e = get_engine()
        _session_local = sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=e)
    return _session_local()


def get_db() -> Generator[Session, None, None]:
    db: Session = get_session()
    try:
        yield db
    finally:
        # release connection back to pool
        db.close()


if _engine is None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
